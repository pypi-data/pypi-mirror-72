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
            depth--;
            if (depth !== 0) {
                depthEntries.set(threadId, depth);
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJhZ2VudC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTs7O0FDQUEsTUFBTSxLQUFLO0lBQVg7UUFDWSxhQUFRLEdBQUcsSUFBSSxHQUFHLEVBQStCLENBQUM7UUFDbEQsZUFBVSxHQUFHLElBQUksR0FBRyxFQUFvQixDQUFDO1FBQ3pDLGVBQVUsR0FBZSxFQUFFLENBQUM7UUFDNUIsV0FBTSxHQUFHLENBQUMsQ0FBQztRQUNYLFlBQU8sR0FBRyxJQUFJLENBQUMsR0FBRyxFQUFFLENBQUM7UUFFckIsa0JBQWEsR0FBaUIsRUFBRSxDQUFDO1FBQ2pDLGVBQVUsR0FBUSxJQUFJLENBQUM7UUFFdkIseUJBQW9CLEdBQXVCLElBQUksQ0FBQztRQUNoRCx1QkFBa0IsR0FBdUIsSUFBSSxDQUFDO1FBZ2dCOUMsVUFBSyxHQUFHLEdBQUcsRUFBRTtZQUNqQixJQUFJLElBQUksQ0FBQyxVQUFVLEtBQUssSUFBSSxFQUFFO2dCQUMxQixZQUFZLENBQUMsSUFBSSxDQUFDLFVBQVUsQ0FBQyxDQUFDO2dCQUM5QixJQUFJLENBQUMsVUFBVSxHQUFHLElBQUksQ0FBQzthQUMxQjtZQUVELElBQUksSUFBSSxDQUFDLGFBQWEsQ0FBQyxNQUFNLEtBQUssQ0FBQyxFQUFFO2dCQUNqQyxPQUFPO2FBQ1Y7WUFFRCxNQUFNLE1BQU0sR0FBRyxJQUFJLENBQUMsYUFBYSxDQUFDO1lBQ2xDLElBQUksQ0FBQyxhQUFhLEdBQUcsRUFBRSxDQUFDO1lBRXhCLElBQUksQ0FBQztnQkFDRCxJQUFJLEVBQUUsWUFBWTtnQkFDbEIsTUFBTTthQUNULENBQUMsQ0FBQztRQUNQLENBQUMsQ0FBQztJQXVCTixDQUFDO0lBdGlCRyxJQUFJLENBQUMsS0FBWSxFQUFFLFVBQTJCLEVBQUUsV0FBeUIsRUFBRSxJQUFlO1FBQ3RGLE1BQU0sQ0FBQyxHQUFHLE1BQW1DLENBQUM7UUFDOUMsQ0FBQyxDQUFDLEtBQUssR0FB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QUFDLENBQUMsQ0FBQyxFQUFFLEVBQUUsQ0FBQztLQUNsQyxDQUFDO0FBQ04sQ0FBQztBQUVELFNBQVMsNkJBQTZCLENBQUMsS0FBcUI7SUFDeEQsT0FBTztRQUNILE1BQU0sRUFBRSxLQUFLLENBQUMsTUFBTTtRQUNwQixPQUFPLEVBQUUsSUFBSSxHQUFHLENBQ1osS0FBSyxDQUFDLE9BQU8sQ0FBQyxHQUFHLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyxDQUFDLEtBQUssQ0FBQyxJQUFJLEVBQUUsNkJBQTZCLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQyxDQUFDO0tBQ3RGLENBQUM7QUFDTixDQUFDO0FBRUQsU0FBUyw2QkFBNkIsQ0FBQyxLQUFxQjtJQUN4RCxPQUFPO1FBQ0gsT0FBTyxFQUFFLElBQUksR0FBRyxDQUNaLEtBQUssQ0FBQyxPQUFPLENBQUMsR0FBRyxDQUFDLFFBQVEsQ0FBQyxFQUFFLENBQUMsQ0FBQyxnQ0FBZ0MsQ0FBQyxRQUFRLENBQUMsRUFBRSxRQUFRLENBQUMsQ0FBQyxDQUFDO0tBQzdGLENBQUM7QUFDTixDQUFDO0FBRUQsU0FBUyxnQ0FBZ0MsQ0FBQyxRQUFnQjtJQUN0RCxNQUFNLGNBQWMsR0FBRyxRQUFRLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxDQUFDO0lBQzdDLE9BQU8sQ0FBQyxjQUFjLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsUUFBUSxDQUFDLENBQUMsQ0FBQyxRQUFRLENBQUMsTUFBTSxDQUFDLENBQUMsRUFBRSxjQUFjLENBQUMsQ0FBQztBQUNuRixDQUFDO0FBRUQsU0FBUyxJQUFJLENBQUksS0FBVSxFQUFFLFNBQW9DO0lBQzdELEtBQUssTUFBTSxPQUFPLElBQUksS0FBSyxFQUFFO1FBQ3pCLElBQUksU0FBUyxDQUFDLE9BQU8sQ0FBQyxFQUFFO1lBQ3BCLE9BQU8sT0FBTyxDQUFDO1NBQ2xCO0tBQ0o7QUFDTCxDQUFDO0FBRUQsU0FBUyxJQUFJO0FBQ2IsQ0FBQztBQTBHRDs7R0FFRztBQUVILE1BQU0sS0FBSyxHQUFHLElBQUksS0FBSyxFQUFFLENBQUM7QUFFMUIsR0FBRyxDQUFDLE9BQU8sR0FBRztJQUNWLElBQUksRUFBRSxLQUFLLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUM7SUFDNUIsT0FBTyxFQUFFLEtBQUssQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQztJQUNsQyxNQUFNLEVBQUUsS0FBSyxDQUFDLE1BQU0sQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDO0NBQ25DLENBQUMiLCJmaWxlIjoiZ2VuZXJhdGVkLmpzIiwic291cmNlUm9vdCI6IiJ9
