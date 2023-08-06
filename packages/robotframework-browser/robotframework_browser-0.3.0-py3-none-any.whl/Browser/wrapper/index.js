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
function createBrowserState(browserType) {
    return __awaiter(this, void 0, void 0, function () {
        var headless, browser, context, page;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    headless = true;
                    if (!(browserType === 'firefox')) return [3 /*break*/, 2];
                    return [4 /*yield*/, playwright_1.firefox.launch({ headless: headless })];
                case 1:
                    browser = _a.sent();
                    return [3 /*break*/, 7];
                case 2:
                    if (!(browserType === 'chrome')) return [3 /*break*/, 4];
                    return [4 /*yield*/, playwright_1.chromium.launch({ headless: headless })];
                case 3:
                    browser = _a.sent();
                    return [3 /*break*/, 7];
                case 4:
                    if (!(browserType === 'webkit')) return [3 /*break*/, 6];
                    return [4 /*yield*/, playwright_1.webkit.launch()];
                case 5:
                    browser = _a.sent();
                    return [3 /*break*/, 7];
                case 6: throw new Error('unsupported browser');
                case 7: return [4 /*yield*/, browser.newContext()];
                case 8:
                    context = _a.sent();
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
    // current open browsers main context and open page
    PlaywrightServer.prototype.openUrl = function (url, callback) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to open URl but had no browser open');
                        return [4 /*yield*/, this.browserState.page.goto(url)];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
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
            var browserType, url, _a, response;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        browserType = call.request.getBrowser();
                        url = call.request.getUrl();
                        console.log('Open browser: ' + browserType);
                        // TODO: accept a flag for headlessness
                        _a = this;
                        return [4 /*yield*/, createBrowserState(browserType)];
                    case 1:
                        // TODO: accept a flag for headlessness
                        _a.browserState = _b.sent();
                        response = new playwright_pb_1.Response.Empty();
                        if (!url) return [3 /*break*/, 3];
                        return [4 /*yield*/, this.openUrl(url, callback)];
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
                        url = call.request.getUrl();
                        console.log('Go to URL: ' + url);
                        return [4 /*yield*/, this.openUrl(url, callback)];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Succesfully opened URL');
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
                        return [4 /*yield*/, this.browserState.page.title()];
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
                        return [4 /*yield*/, this.browserState.page.textContent(selector)];
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
                        return [4 /*yield*/, this.browserState.page.$(selector)];
                    case 1:
                        element = _a.sent();
                        exists(element, callback, "Couldn't find element: " + selector);
                        return [4 /*yield*/, element.getProperty(property)];
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
                        return [4 /*yield*/, this.browserState.page.$(selector)];
                    case 1:
                        element = _a.sent();
                        exists(element, callback, "Couldn't find element: " + selector);
                        return [4 /*yield*/, element.getProperty(property)];
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
            var inputText, selector, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to input text, no open browser');
                        inputText = call.request.getInput();
                        selector = call.request.getSelector();
                        return [4 /*yield*/, this.browserState.page.fill(selector, inputText)];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Input text: ' + inputText);
                        callback(null, response);
                        return [2 /*return*/];
                }
            });
        });
    };
    PlaywrightServer.prototype.clickButton = function (call, callback) {
        return __awaiter(this, void 0, void 0, function () {
            var selector, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        exists(this.browserState, callback, 'Tried to click button, no open browser');
                        selector = call.request.getSelector();
                        return [4 /*yield*/, this.browserState.page.click(selector)];
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
                        return [4 /*yield*/, this.browserState.page.check(selector)];
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
                        return [4 /*yield*/, this.browserState.page.uncheck(selector)];
                    case 1:
                        _a.sent();
                        response = emptyWithLog('Unhecked checkbox: ' + selector);
                        callback(null, response);
                        return [2 /*return*/];
                }
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
                        return [4 /*yield*/, this.browserState.page.screenshot({ path: path })];
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
