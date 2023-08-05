(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("@finos/perspective"));
	else if(typeof define === 'function' && define.amd)
		define(["@finos/perspective"], factory);
	else {
		var a = typeof exports === 'object' ? factory(require("@finos/perspective")) : factory(root["@finos/perspective"]);
		for(var i in a) (typeof exports === 'object' ? exports : root)[i] = a[i];
	}
})(global, function(__WEBPACK_EXTERNAL_MODULE__finos_perspective__) {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./js/server.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./js/server.js":
/*!**********************!*\
  !*** ./js/server.js ***!
  \**********************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("var zerorpc = __webpack_require__(!(function webpackMissingModule() { var e = new Error(\"Cannot find module 'zerorpc'\"); e.code = 'MODULE_NOT_FOUND'; throw e; }()));\nconst perspective = __webpack_require__(/*! @finos/perspective */ \"@finos/perspective\");\n\nvar views = {};\nvar view_counter = 0;\nvar table;\n\nvar server = new zerorpc.Server({\n    heartbeat: function(reply) {\n        reply(null, \"pong\");\n    },\n    table: function(data, options, reply) {\n        if (table) {\n            table.delete();\n        }\n        table = perspective.table(data, options);\n        reply(null, \"\");\n    },\n    update: function(data, reply) {\n        if (!table) {\n            return;\n        }\n        if (!Array.isArray(data)) {\n            data = [data];\n        }\n        table.update(data);\n        reply(null, \"\");\n    },\n    remove: function(data, reply) {\n        if (!table) {\n            return;\n        }\n        table.remove(data);\n        reply(null, \"\");\n    },\n    view: function(config, reply) {\n        if (!table) {\n            return;\n        }\n        views[view_counter] = table.view(config);\n        reply(null, view_counter);\n        view_counter++;\n    },\n    to_json: function(data, reply) {\n        if (!table) {\n            return;\n        }\n        if (data >= 0) {\n            views[data].to_json().then(json => reply(null, json));\n        } else {\n            table\n                .view({})\n                .to_json()\n                .then(json => reply(null, json));\n        }\n    },\n    to_columns: function(data, reply) {\n        if (!table) {\n            return;\n        }\n        if (data >= 0) {\n            views[data].to_columns().then(json => reply(null, json));\n        } else {\n            table\n                .view({})\n                .to_columns()\n                .then(json => reply(null, json));\n        }\n    }\n});\n\nserver.bind(\"tcp://\" + process.env.PERSPECTIVE_NODE_HOST);\n\n\n//# sourceURL=webpack:///./js/server.js?");

/***/ }),

/***/ "@finos/perspective":
/*!*************************************!*\
  !*** external "@finos/perspective" ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("module.exports = __WEBPACK_EXTERNAL_MODULE__finos_perspective__;\n\n//# sourceURL=webpack:///external_%22@finos/perspective%22?");

/***/ })

/******/ });
});