(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
(function (global){
"use strict";
class Agent {
    constructor() {
        this.handlers = new Map();
        this.stackDepth = new Map();
        this.traceState = {};
        this.nextId = 1;
        this.started = Date.now();
        this.pendingEvents = [];
        this.flushTimer = null;
        this.cachedModuleResolver = null;
        this.cachedObjcResolver = null;
        this.flush = () => {
            if (this.flushTimer !== null) {
                clearTimeout(this.flushTimer);
                this.flushTimer = null;
            }
            if (this.pendingEvents.length === 0) {
                return;
            }
            const events = this.pendingEvents;
            this.pendingEvents = [];
            send({
                type: "events:add",
                events
            });
        };
    }
    init(stage, parameters, initScripts, spec) {
        const g = global;
        g.stage = stage;
        g.parameters = parameters;
        g.state = this.traceState;
        for (const script of initScripts) {
            try {
                (1, eval)(script.source);
            }
            catch (e) {
                throw new Error(`Unable to load ${script.filename}: ${e.stack}`);
            }
        }
        this.start(spec).catch(e => {
            send({
                type: "agent:error",
                message: e.message
            });
        });
    }
    dispose() {
        this.flush();
    }
    update(id, name, script) {
        const handler = this.handlers.get(id);
        if (handler === undefined) {
            throw new Error("Invalid target ID");
        }
        const newHandler = this.parseHandler(name, script);
        handler[0] = newHandler[0];
        handler[1] = newHandler[1];
    }
    async start(spec) {
        const plan = {
            native: new Map(),
            java: []
        };
        const javaEntries = [];
        for (const [operation, scope, pattern] of spec) {
            switch (scope) {
                case "module":
                    if (operation === "include") {
                        this.includeModule(pattern, plan);
                    }
                    else {
                        this.excludeModule(pattern, plan);
                    }
                    break;
                case "function":
                    if (operation === "include") {
                        this.includeFunction(pattern, plan);
                    }
                    else {
                        this.excludeFunction(pattern, plan);
                    }
                    break;
                case "relative-function":
                    if (operation === "include") {
                        this.includeRelativeFunction(pattern, plan);
                    }
                    break;
                case "imports":
                    if (operation === "include") {
                        this.includeImports(pattern, plan);
                    }
                    break;
                case "objc-method":
                    if (operation === "include") {
                        this.includeObjCMethod(pattern, plan);
                    }
                    else {
                        this.excludeObjCMethod(pattern, plan);
                    }
                    break;
                case "java-method":
                    javaEntries.push([operation, pattern]);
                    break;
                case "debug-symbol":
                    if (operation === "include") {
                        this.includeDebugSymbol(pattern, plan);
                    }
                    break;
            }
        }
        let javaStartRequest;
        let javaStartDeferred = true;
        if (javaEntries.length > 0) {
            if (!Java.available) {
                throw new Error("Java runtime is not available");
            }
            javaStartRequest = new Promise((resolve, reject) => {
                Java.perform(() => {
                    javaStartDeferred = false;
                    for (const [operation, pattern] of javaEntries) {
                        if (operation === "include") {
                            this.includeJavaMethod(pattern, plan);
                        }
                        else {
                            this.excludeJavaMethod(pattern, plan);
                        }
                    }
                    this.traceJavaTargets(plan.java).then(resolve).catch(reject);
                });
            });
        }
        else {
            javaStartRequest = Promise.resolve();
        }
        await this.traceNativeTargets(plan.native);
        if (!javaStartDeferred) {
            await javaStartRequest;
        }
        send({
            type: "agent:initialized"
        });
        javaStartRequest.then(() => {
            send({
                type: "agent:started",
                count: this.handlers.size
            });
        });
    }
    async traceNativeTargets(targets) {
        const cGroups = new Map();
        const objcGroups = new Map();
        for (const [id, [type, scope, name]] of targets.entries()) {
            const entries = (type === "objc") ? objcGroups : cGroups;
            let group = entries.get(scope);
            if (group === undefined) {
                group = [];
                entries.set(scope, group);
            }
            group.push([name, ptr(id)]);
        }
        return await Promise.all([
            this.traceNativeEntries("c", cGroups),
            this.traceNativeEntries("objc", objcGroups)
        ]);
    }
    async traceNativeEntries(flavor, groups) {
        if (groups.size === 0) {
            return;
        }
        const baseId = this.nextId;
        const scopes = [];
        const request = {
            type: "handlers:get",
            flavor,
            baseId,
            scopes
        };
        for (const [name, items] of groups.entries()) {
            scopes.push({
                name,
                members: items.map(item => item[0])
            });
            this.nextId += items.length;
        }
        const { scripts } = await getHandlers(request);
        let offset = 0;
        for (const items of groups.values()) {
            for (const [name, address] of items) {
                const id = baseId + offset;
                const displayName = (typeof name === "string") ? name : name[1];
                const handler = this.parseHandler(displayName, scripts[offset]);
                this.handlers.set(id, handler);
                try {
                    Interceptor.attach(address, this.makeNativeListenerCallbacks(id, handler));
                }
                catch (e) {
                    send({
                        type: "agent:warning",
                        message: `Skipping "${name}": ${e.message}`
                    });
                }
                offset++;
            }
        }
    }
    async traceJavaTargets(groups) {
        const baseId = this.nextId;
        const scopes = [];
        const request = {
            type: "handlers:get",
            flavor: "java",
            baseId,
            scopes
        };
        for (const group of groups) {
            for (const [className, { methods }] of group.classes.entries()) {
                const classNameParts = className.split(".");
                const bareClassName = classNameParts[classNameParts.length - 1];
                const members = Array.from(methods.keys()).map(bareName => [bareName, `${bareClassName}.${bareName}`]);
                scopes.push({
                    name: className,
                    members
                });
                this.nextId += members.length;
            }
        }
        const { scripts } = await getHandlers(request);
        return new Promise(resolve => {
            Java.perform(() => {
                let offset = 0;
                for (const group of groups) {
                    const factory = Java.ClassFactory.get(group.loader);
                    for (const [className, { methods }] of group.classes.entries()) {
                        const C = factory.use(className);
                        for (const [bareName, fullName] of methods.entries()) {
                            const id = baseId + offset;
                            const handler = this.parseHandler(fullName, scripts[offset]);
                            this.handlers.set(id, handler);
                            const dispatcher = C[bareName];
                            for (const method of dispatcher.overloads) {
                                method.implementation = this.makeJavaMethodWrapper(id, method, handler);
                            }
                            offset++;
                        }
                    }
                }
                resolve();
            });
        });
    }
    makeNativeListenerCallbacks(id, handler) {
        const agent = this;
        return {
            onEnter(args) {
                agent.invokeNativeHandler(id, handler[0], this, args, ">");
            },
            onLeave(retval) {
                agent.invokeNativeHandler(id, handler[1], this, retval, "<");
            }
        };
    }
    makeJavaMethodWrapper(id, method, handler) {
        const agent = this;
        return function (...args) {
            return agent.handleJavaInvocation(id, method, handler, this, args);
        };
    }
    handleJavaInvocation(id, method, handler, instance, args) {
        this.invokeJavaHandler(id, handler[0], instance, args, ">");
        const retval = method.apply(instance, args);
        const replacementRetval = this.invokeJavaHandler(id, handler[1], instance, retval, "<");
        return (replacementRetval !== undefined) ? replacementRetval : retval;
    }
    invokeNativeHandler(id, callback, context, param, cutPoint) {
        const timestamp = Date.now() - this.started;
        const threadId = context.threadId;
        const depth = this.updateDepth(threadId, cutPoint);
        const log = (...message) => {
            this.emit([id, timestamp, threadId, depth, message.join(" ")]);
        };
        callback.call(context, log, param, this.traceState);
    }
    invokeJavaHandler(id, callback, instance, param, cutPoint) {
        const timestamp = Date.now() - this.started;
        const threadId = Process.getCurrentThreadId();
        const depth = this.updateDepth(threadId, cutPoint);
        const log = (...message) => {
            this.emit([id, timestamp, threadId, depth, message.join(" ")]);
        };
        try {
            return callback.call(instance, log, param, this.traceState);
        }
        catch (e) {
            const isJavaException = e.$h !== undefined;
            if (isJavaException) {
                throw e;
            }
            else {
                Script.nextTick(() => { throw e; });
            }
        }
    }
    updateDepth(threadId, cutPoint) {
        const depthEntries = this.stackDepth;
        let depth = depthEntries.get(threadId) ?? 0;
        if (cutPoint === ">") {
            depthEntries.set(threadId, depth + 1);
        }
        else {
            if (depth !== 0) {
                depthEntries.set(threadId, depth - 1);
            }
            else {
                depthEntries.delete(threadId);
            }
        }
        return depth;
    }
    parseHandler(name, script) {
        try {
            const h = (1, eval)("(" + script + ")");
            return [h.onEnter ?? noop, h.onLeave ?? noop];
        }
        catch (e) {
            send({
                type: "agent:warning",
                message: `Invalid handler for "${name}": ${e.message}`
            });
            return [noop, noop];
        }
    }
    includeModule(pattern, plan) {
        const { native } = plan;
        for (const m of this.getModuleResolver().enumerateMatches(`exports:${pattern}!*`)) {
            native.set(m.address.toString(), moduleFunctionTargetFromMatch(m));
        }
    }
    excludeModule(pattern, plan) {
        const { native } = plan;
        for (const m of this.getModuleResolver().enumerateMatches(`exports:${pattern}!*`)) {
            native.delete(m.address.toString());
        }
    }
    includeFunction(pattern, plan) {
        const e = parseModuleFunctionPattern(pattern);
        const { native } = plan;
        for (const m of this.getModuleResolver().enumerateMatches(`exports:${e.module}!${e.function}`)) {
            native.set(m.address.toString(), moduleFunctionTargetFromMatch(m));
        }
    }
    excludeFunction(pattern, plan) {
        const e = parseModuleFunctionPattern(pattern);
        const { native } = plan;
        for (const m of this.getModuleResolver().enumerateMatches(`exports:${e.module}!${e.function}`)) {
            native.delete(m.address.toString());
        }
    }
    includeRelativeFunction(pattern, plan) {
        const e = parseRelativeFunctionPattern(pattern);
        const address = Module.getBaseAddress(e.module).add(e.offset);
        plan.native.set(address.toString(), ["c", e.module, `sub_${e.offset.toString(16)}`]);
    }
    includeImports(pattern, plan) {
        let matches;
        if (pattern === null) {
            const mainModule = Process.enumerateModules()[0].path;
            matches = this.getModuleResolver().enumerateMatches(`imports:${mainModule}!*`);
        }
        else {
            matches = this.getModuleResolver().enumerateMatches(`imports:${pattern}!*`);
        }
        const { native } = plan;
        for (const m of matches) {
            native.set(m.address.toString(), moduleFunctionTargetFromMatch(m));
        }
    }
    includeObjCMethod(pattern, plan) {
        const { native } = plan;
        for (const m of this.getObjcResolver().enumerateMatches(pattern)) {
            native.set(m.address.toString(), objcMethodTargetFromMatch(m));
        }
    }
    excludeObjCMethod(pattern, plan) {
        const { native } = plan;
        for (const m of this.getObjcResolver().enumerateMatches(pattern)) {
            native.delete(m.address.toString());
        }
    }
    includeJavaMethod(pattern, plan) {
        const existingGroups = plan.java;
        const groups = Java.enumerateMethods(pattern);
        for (const group of groups) {
            const { loader } = group;
            const existingGroup = find(existingGroups, candidate => {
                const { loader: candidateLoader } = candidate;
                if (candidateLoader !== null && loader !== null) {
                    return candidateLoader.equals(loader);
                }
                else {
                    return candidateLoader === loader;
                }
            });
            if (existingGroup === undefined) {
                existingGroups.push(javaTargetGroupFromMatchGroup(group));
                continue;
            }
            const { classes: existingClasses } = existingGroup;
            for (const klass of group.classes) {
                const { name: className } = klass;
                const existingClass = existingClasses.get(className);
                if (existingClass === undefined) {
                    existingClasses.set(className, javaTargetClassFromMatchClass(klass));
                    continue;
                }
                const { methods: existingMethods } = existingClass;
                for (const methodName of klass.methods) {
                    const bareMethodName = javaBareMethodNameFromMethodName(methodName);
                    const existingName = existingMethods.get(bareMethodName);
                    if (existingName === undefined) {
                        existingMethods.set(bareMethodName, methodName);
                    }
                    else {
                        existingMethods.set(bareMethodName, (methodName.length > existingName.length) ? methodName : existingName);
                    }
                }
            }
        }
    }
    excludeJavaMethod(pattern, plan) {
        const existingGroups = plan.java;
        const groups = Java.enumerateMethods(pattern);
        for (const group of groups) {
            const { loader } = group;
            const existingGroup = find(existingGroups, candidate => {
                const { loader: candidateLoader } = candidate;
                if (candidateLoader !== null && loader !== null) {
                    return candidateLoader.equals(loader);
                }
                else {
                    return candidateLoader === loader;
                }
            });
            if (existingGroup === undefined) {
                continue;
            }
            const { classes: existingClasses } = existingGroup;
            for (const klass of group.classes) {
                const { name: className } = klass;
                const existingClass = existingClasses.get(className);
                if (existingClass === undefined) {
                    continue;
                }
                const { methods: existingMethods } = existingClass;
                for (const methodName of klass.methods) {
                    const bareMethodName = javaBareMethodNameFromMethodName(methodName);
                    existingMethods.delete(bareMethodName);
                }
            }
        }
    }
    includeDebugSymbol(pattern, plan) {
        const { native } = plan;
        for (const address of DebugSymbol.findFunctionsMatching(pattern)) {
            native.set(address.toString(), debugSymbolTargetFromAddress(address));
        }
    }
    emit(event) {
        this.pendingEvents.push(event);
        if (this.flushTimer === null) {
            this.flushTimer = setTimeout(this.flush, 50);
        }
    }
    getModuleResolver() {
        let resolver = this.cachedModuleResolver;
        if (resolver === null) {
            resolver = new ApiResolver("module");
            this.cachedModuleResolver = resolver;
        }
        return resolver;
    }
    getObjcResolver() {
        let resolver = this.cachedObjcResolver;
        if (resolver === null) {
            try {
                resolver = new ApiResolver("objc");
            }
            catch (e) {
                throw new Error("Objective-C runtime is not available");
            }
            this.cachedModuleResolver = resolver;
        }
        return resolver;
    }
}
async function getHandlers(request) {
    const scripts = [];
    const { type, flavor, baseId } = request;
    const pendingScopes = request.scopes.slice().map(({ name, members }) => {
        return {
            name,
            members: members.slice()
        };
    });
    let id = baseId;
    do {
        const curScopes = [];
        const curRequest = {
            type,
            flavor,
            baseId: id,
            scopes: curScopes
        };
        let size = 0;
        for (const { name, members: pendingMembers } of pendingScopes) {
            const curMembers = [];
            curScopes.push({
                name,
                members: curMembers
            });
            let exhausted = false;
            for (const member of pendingMembers) {
                curMembers.push(member);
                size++;
                if (size === 1000) {
                    exhausted = true;
                    break;
                }
            }
            pendingMembers.splice(0, curMembers.length);
            if (exhausted) {
                break;
            }
        }
        while (pendingScopes.length !== 0 && pendingScopes[0].members.length === 0) {
            pendingScopes.splice(0, 1);
        }
        send(curRequest);
        const response = await receiveResponse(`reply:${id}`);
        scripts.push(...response.scripts);
        id += size;
    } while (pendingScopes.length !== 0);
    return {
        scripts
    };
}
function receiveResponse(type) {
    return new Promise(resolve => {
        recv(type, (response) => {
            resolve(response);
        });
    });
}
function moduleFunctionTargetFromMatch(m) {
    const [modulePath, functionName] = m.name.split("!", 2);
    return ["c", modulePath, functionName];
}
function objcMethodTargetFromMatch(m) {
    const { name } = m;
    const [className, methodName] = name.substr(2, name.length - 3).split(" ", 2);
    return ["objc", className, [methodName, name]];
}
function debugSymbolTargetFromAddress(address) {
    const symbol = DebugSymbol.fromAddress(address);
    return ["c", symbol.moduleName ?? "", symbol.name];
}
function parseModuleFunctionPattern(pattern) {
    const tokens = pattern.split("!", 2);
    let m, f;
    if (tokens.length === 1) {
        m = "*";
        f = tokens[0];
    }
    else {
        m = (tokens[0] === "") ? "*" : tokens[0];
        f = (tokens[1] === "") ? "*" : tokens[1];
    }
    return {
        module: m,
        function: f
    };
}
function parseRelativeFunctionPattern(pattern) {
    const tokens = pattern.split("!", 2);
    return {
        module: tokens[0],
        offset: parseInt(tokens[1], 16)
    };
}
function javaTargetGroupFromMatchGroup(group) {
    return {
        loader: group.loader,
        classes: new Map(group.classes.map(klass => [klass.name, javaTargetClassFromMatchClass(klass)]))
    };
}
function javaTargetClassFromMatchClass(klass) {
    return {
        methods: new Map(klass.methods.map(fullName => [javaBareMethodNameFromMethodName(fullName), fullName]))
    };
}
function javaBareMethodNameFromMethodName(fullName) {
    const signatureStart = fullName.indexOf("(");
    return (signatureStart === -1) ? fullName : fullName.substr(0, signatureStart);
}
function find(array, predicate) {
    for (const element of array) {
        if (predicate(element)) {
            return element;
        }
    }
}
function noop() {
}
/*
 * ^^^
 */
const agent = new Agent();
rpc.exports = {
    init: agent.init.bind(agent),
    dispose: agent.dispose.bind(agent),
    update: agent.update.bind(agent)
};

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJhZ2VudC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTs7O0FDQUEsTUFBTSxLQUFLO0lBQVg7UUFDWSxhQUFRLEdBQUcsSUFBSSxHQUFHLEVBQStCLENBQUM7UUFDbEQsZUFBVSxHQUFHLElBQUksR0FBRyxFQUFvQixDQUFDO1FBQ3pDLGVBQVUsR0FBZSxFQUFFLENBQUM7UUFDNUIsV0FBTSxHQUFHLENBQUMsQ0FBQztRQUNYLFlBQU8sR0FBRyxJQUFJLENBQUMsR0FBRyxFQUFFLENBQUM7UUFFckIsa0JBQWEsR0FBaUIsRUFBRSxDQUFDO1FBQ2pDLGVBQVUsR0FBUSxJQUFJLENBQUM7UUFFdkIseUJBQW9CLEdBQXVCLElBQUksQ0FBQztRQUNoRCx1QkFBa0IsR0FBdUIsSUFBSSxDQUFDO1FBK2Y5QyxVQUFLLEdBQUcsR0FBRyxFQUFFO1lBQ2pCLElBQUksSUFBSSxDQUFDLFVBQVUsS0FBSyxJQUFJLEVBQUU7Z0JBQzFCLFlBQVksQ0FBQyxJQUFJLENBQUMsVUFBVSxDQUFDLENBQUM7Z0JBQzlCLElBQUksQ0FBQyxVQUFVLEdBQUcsSUFBSSxDQUFDO2FBQzFCO1lBRUQsSUFBSSxJQUFJLENBQUMsYUFBYSxDQUFDLE1BQU0sS0FBSyxDQUFDLEVBQUU7Z0JBQ2pDLE9BQU87YUFDVjtZQUVELE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxhQUFhLENBQUM7WUFDbEMsSUFBSSxDQUFDLGFBQWEsR0FBRyxFQUFFLENBQUM7WUFFeEIsSUFBSSxDQUFDO2dCQUNELElBQUksRUFBRSxZQUFZO2dCQUNsQixNQUFNO2FBQ1QsQ0FBQyxDQUFDO1FBQ1AsQ0FBQyxDQUFDO0lBdUJOLENBQUM7SUFyaUJHLElBQUksQ0FBQyxLQUFZLEVBQUUsVUFBMkIsRUFBRSxXQUF5QixFQUFFLElBQWU7UUFDdEYsTUFBTSxDQUFDLEdBQUcsTUFBbUMsQ0FBQztRQUM5QyxDQUFDLENBQUMsS0FBSyxHQUFH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QUMsRUFBRSxFQUFFLENBQUM7S0FDbEMsQ0FBQztBQUNOLENBQUM7QUFFRCxTQUFTLDZCQUE2QixDQUFDLEtBQXFCO0lBQ3hELE9BQU87UUFDSCxNQUFNLEVBQUUsS0FBSyxDQUFDLE1BQU07UUFDcEIsT0FBTyxFQUFFLElBQUksR0FBRyxDQUNaLEtBQUssQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsQ0FBQyxLQUFLLENBQUMsSUFBSSxFQUFFLDZCQUE2QixDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQztLQUN0RixDQUFDO0FBQ04sQ0FBQztBQUVELFNBQVMsNkJBQTZCLENBQUMsS0FBcUI7SUFDeEQsT0FBTztRQUNILE9BQU8sRUFBRSxJQUFJLEdBQUcsQ0FDWixLQUFLLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsRUFBRSxDQUFDLENBQUMsZ0NBQWdDLENBQUMsUUFBUSxDQUFDLEVBQUUsUUFBUSxDQUFDLENBQUMsQ0FBQztLQUM3RixDQUFDO0FBQ04sQ0FBQztBQUVELFNBQVMsZ0NBQWdDLENBQUMsUUFBZ0I7SUFDdEQsTUFBTSxjQUFjLEdBQUcsUUFBUSxDQUFDLE9BQU8sQ0FBQyxHQUFHLENBQUMsQ0FBQztJQUM3QyxPQUFPLENBQUMsY0FBYyxLQUFLLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLFFBQVEsQ0FBQyxDQUFDLENBQUMsUUFBUSxDQUFDLE1BQU0sQ0FBQyxDQUFDLEVBQUUsY0FBYyxDQUFDLENBQUM7QUFDbkYsQ0FBQztBQUVELFNBQVMsSUFBSSxDQUFJLEtBQVUsRUFBRSxTQUFvQztJQUM3RCxLQUFLLE1BQU0sT0FBTyxJQUFJLEtBQUssRUFBRTtRQUN6QixJQUFJLFNBQVMsQ0FBQyxPQUFPLENBQUMsRUFBRTtZQUNwQixPQUFPLE9BQU8sQ0FBQztTQUNsQjtLQUNKO0FBQ0wsQ0FBQztBQUVELFNBQVMsSUFBSTtBQUNiLENBQUM7QUEwR0Q7O0dBRUc7QUFFSCxNQUFNLEtBQUssR0FBRyxJQUFJLEtBQUssRUFBRSxDQUFDO0FBRTFCLEdBQUcsQ0FBQyxPQUFPLEdBQUc7SUFDVixJQUFJLEVBQUUsS0FBSyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDO0lBQzVCLE9BQU8sRUFBRSxLQUFLLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUM7SUFDbEMsTUFBTSxFQUFFLEtBQUssQ0FBQyxNQUFNLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQztDQUNuQyxDQUFDIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIifQ==
