"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var playwright_grpc_pb_1 = require("./generated/playwright_grpc_pb");
var playwright_1 = require("playwright");
var grpc_1 = require("grpc");
var playwright_pb_1 = require("./generated/playwright_pb");
// This is necessary for improved typescript inference
/*
 * If obj is not trueish call callback with new Error containing message
 */
function exists(obj, callback, message) {
    if (!obj) {
        callback(new Error(message), null);
    }
}
// Can't have an async constructor, this is a workaround
function createBrowserState(browserType, headless) {
    return __awaiter(this, void 0, void 0, function () {
        var browser, context, page;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!(browserType === 'firefox')) return [3 /*break*/, 2];
                    return [4 /*yield*/, playwright_1.firefox.launch({ headless: headless })];
                case 1:
                    browser = _a.sent();
                    return [3 /*break*/, 7];
                case 2:
                    if (!(browserType === 'chromium')) return [3 /*break*/, 4];
                    return [4 /*yield*/, playwright_1.chromium.launch({ headless: headless })];
                case 3:
                    browser = _a.sent();
                    return [3 /*break*/, 7];
                case 4:
                    if (!(browserType === 'webkit')) return [3 /*break*/, 6];
                    return [4 /*yield*/, playwright_1.webkit.launch({ headless: headless })];
                case 5:
                    browser = _a.sent();
                    return [3 /*break*/, 7];
                case 6: throw new Error('unsupported browser');
                case 7: return [4 /*yield*/, browser.newContext()];
                case 8:
                    context = _a.sent();
                    context.setDefaultTimeout(parseFloat(process.env.TIMEOUT || '10000'));
                    return [4 /*yield*/, context.newPage()];
                case 9:
                    page = _a.sent();
                    return [2 /*return*/, new BrowserState(browser, context, page)];
            }
        });
    });
}
var BrowserState = /** @class */ (function () {
    function BrowserState(browser, context, page) {
        this.browser = browser;
        this.context = context;
        this.page = page;
    }
    return BrowserState;
}());
function emptyWithLog(text) {
    var response = new playwright_pb_1.Response.Empty();
    response.setLog(text);
    return response;
}
var PlaywrightServer = /** @class */ (function () {
    function PlaywrightServer() {
    }
    PlaywrightServer.prototype.closeBrowser = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to close browser but none was open');
                        return [4 /*yield*/, this.browserState.browser.close()];
                    case 1:
                        _a.sent();
                        this.browserState = undefined;
                        console.log('Closed browser');
                        response = emptyWithLog('Closed browser');
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.openBrowser = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var browserType, url, headless, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        browserType = call.request.getBrowser();
                        url = call.request.getUrl();
                        headless = call.request.getHeadless();
                        console.log('Open browser: ' + browserType);
                        _a = this;
                        return [4 /*yield*/, createBrowserState(browserType, headless)];
                    case 1:
                        _a.browserState = _b.sent();
                        if (!url) return [3 /*break*/, 3];
                        return [4 /*yield*/, this.browserState.page.goto(url)];
                    case 2:
                        _b.sent();
                        callback(null, emptyWithLog("Succesfully opened browser " + browserType + " to " + url + "."));
                        return [3 /*break*/, 4];
                    case 3:
                        callback(null, emptyWithLog("Succesfully opened browser " + browserType + "."));
                        _b.label = 4;
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.goTo = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var url, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to open URl but had no browser open');
                        url = call.request.getUrl();
                        console.log('Go to URL: ' + url);
                        return [4 /*yield*/, this.browserState.page.goto(url).catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Succesfully opened URL');
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.goBack = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to go back in history but no browser was open');
                        return [4 /*yield*/, this.browserState.page.goBack().catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        console.log('Go Back');
                        response = emptyWithLog('Did Go Back');
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.goForward = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to go forward in history but no browser was open');
                        return [4 /*yield*/, this.browserState.page.goForward().catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        console.log('Go BForward');
                        response = emptyWithLog('Did Go Forward');
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.getTitle = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var title, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to get title, no open browser');
                        console.log('Getting title');
                        return [4 /*yield*/, this.browserState.page.title().catch(function (e) {
                                callback(e, null);
                                throw e;
                            })];
                    case 1:
                        title = _a.sent();
                        response = new playwright_pb_1.Response.String();
                        response.setBody(title);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.getUrl = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var url, response;
            return __generator(this, function (_a) {
                exists(this.browserState, callback, 'Tried to get page URL, no open browser');
                console.log('Getting URL');
                url = this.browserState.page.url();
                response = new playwright_pb_1.Response.String();
                response.setBody(url);
                callback(null, response);
                return [2 /*return*/];
            });
        });
    };
    PlaywrightServer.prototype.getTextContent = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, content, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to find text on page, no open browser');
                        selector = call.request.getSelector();
                        return [4 /*yield*/, this.browserState.page.textContent(selector).catch(function (e) {
                                callback(e, null);
                                throw e;
                            })];
                    case 1:
                        content = _a.sent();
                        response = new playwright_pb_1.Response.String();
                        response.setBody((content === null || content === void 0 ? void 0 : content.toString()) || '');
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    // TODO: work some of getDomProperty and getBoolProperty's duplicate code into a root function
    PlaywrightServer.prototype.getDomProperty = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, property, element, result, content, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to get DOM property, no open browser');
                        selector = call.request.getSelector();
                        property = call.request.getProperty();
                        return [4 /*yield*/, this.browserState.page.$(selector).catch(function (e) {
                                callback(e, null);
                                throw e;
                            })];
                    case 1:
                        element = _a.sent();
                        exists(element, callback, "Couldn't find element: " + selector);
                        return [4 /*yield*/, element.getProperty(property).catch(function (e) {
                                callback(e, null);
                                throw e;
                            })];
                    case 2:
                        result = _a.sent();
                        return [4 /*yield*/, result.jsonValue()];
                    case 3:
                        content = _a.sent();
                        console.log("Retrieved dom property for element " + selector + " containing " + content);
                        response = new playwright_pb_1.Response.String();
                        response.setBody(content);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.getBoolProperty = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, property, element, result, content, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to get DOM property, no open browser');
                        selector = call.request.getSelector();
                        property = call.request.getProperty();
                        return [4 /*yield*/, this.browserState.page.$(selector).catch(function (e) {
                                callback(e, null);
                                throw e;
                            })];
                    case 1:
                        element = _a.sent();
                        exists(element, callback, "Couldn't find element: " + selector);
                        return [4 /*yield*/, element.getProperty(property).catch(function (e) {
                                callback(e, null);
                                throw e;
                            })];
                    case 2:
                        result = _a.sent();
                        return [4 /*yield*/, result.jsonValue()];
                    case 3:
                        content = _a.sent();
                        console.log("Retrieved dom property for element " + selector + " containing " + content);
                        response = new playwright_pb_1.Response.Bool();
                        response.setBody(content || false);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.inputText = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var inputText, selector, type, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to input text, no open browser');
                        inputText = call.request.getInput();
                        selector = call.request.getSelector();
                        type = call.request.getType();
                        if (!type) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.browserState.page.type(selector, inputText).catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 2: return [4 /*yield*/, this.browserState.page.fill(selector, inputText).catch(function (e) { return callback(e, null); })];
                    case 3:
                        _a.sent();
                        _a.label = 4;
                    case 4:
                        response = emptyWithLog('Input text: ' + inputText);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.typeText = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, text, delay, clear, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to type text, no open browser');
                        selector = call.request.getSelector();
                        text = call.request.getText();
                        delay = call.request.getDelay();
                        clear = call.request.getClear();
                        if (!clear) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.browserState.page.fill(selector, '').catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        _a.label = 2;
                    case 2: return [4 /*yield*/, this.browserState.page.type(selector, text, { delay: delay }).catch(function (e) { return callback(e, null); })];
                    case 3:
                        _a.sent();
                        response = emptyWithLog('Type text: ' + text);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.fillText = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, text, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to fill text, no open browser');
                        selector = call.request.getSelector();
                        text = call.request.getText();
                        return [4 /*yield*/, this.browserState.page.fill(selector, text).catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Fill text: ' + text);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.clearText = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to clear text field, no open browser');
                        selector = call.request.getSelector();
                        return [4 /*yield*/, this.browserState.page.fill(selector, '').catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Text field cleared.');
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.press = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, keyList, _i, keyList_1, i, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to input text, no open browser');
                        selector = call.request.getSelector();
                        keyList = call.request.getKeyList();
                        _i = 0, keyList_1 = keyList;
                        _a.label = 1;
                    case 1:
                        if (!(_i < keyList_1.length)) return [3 /*break*/, 4];
                        i = keyList_1[_i];
                        return [4 /*yield*/, this.browserState.page.press(selector, i).catch(function (e) { return callback(e, null); })];
                    case 2:
                        _a.sent();
                        _a.label = 3;
                    case 3:
                        _i++;
                        return [3 /*break*/, 1];
                    case 4:
                        response = emptyWithLog('Pressed keys: ' + keyList);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.click = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to click button, no open browser');
                        selector = call.request.getSelector();
                        return [4 /*yield*/, this.browserState.page.click(selector).catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Clicked button: ' + selector);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.checkCheckbox = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to check checkbox, no open browser');
                        selector = call.request.getSelector();
                        return [4 /*yield*/, this.browserState.page.check(selector).catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Checked checkbox: ' + selector);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.uncheckCheckbox = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to uncheck checkbox, no open browser');
                        selector = call.request.getSelector();
                        return [4 /*yield*/, this.browserState.page.uncheck(selector).catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Unhecked checkbox: ' + selector);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.setTimeout = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var timeout, response;
            return __generator(this, function (_a) {
                exists(this.browserState, callback, 'Tried to set timeout, no open browser');
                timeout = call.request.getTimeout();
                this.browserState.context.setDefaultTimeout(timeout);
                response = emptyWithLog('Set timeout to: ' + timeout);
                callback(null, response);
                return [2 /*return*/];
            });
        });
    };
    PlaywrightServer.prototype.health = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                response = new playwright_pb_1.Response.String();
                response.setBody('OK');
                callback(null, response);
                return [2 /*return*/];
            });
        });
    };
    PlaywrightServer.prototype.screenshot = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var path, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to take screenshot, no open browser');
                        path = call.request.getPath() + '.png';
                        console.log("Taking a screenshot of current page to " + path);
                        return [4 /*yield*/, this.browserState.page.screenshot({ path: path }).catch(function (e) { return callback(e, null); })];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Succesfully took screenshot');
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    return PlaywrightServer;
}());
var server = new grpc_1.Server();
server.addService(playwright_grpc_pb_1.PlaywrightService, new PlaywrightServer());
var port = process.env.PORT || '0';
server.bind("localhost:" + port, grpc_1.ServerCredentials.createInsecure());
console.log("Listening on " + port);
server.start();
