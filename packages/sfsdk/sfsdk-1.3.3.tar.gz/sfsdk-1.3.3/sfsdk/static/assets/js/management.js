/*
 *  Copyright (C) 2020 SecureFlag Limited
 *  All Rights Reserved.
 * 
 * NOTICE:  All information contained herein is, and remains the property 
 * of SecureFlag Limited. The intellectual and technical concepts contained 
 * herein are proprietary to SecureFlag Limited and may be covered by EU
 * and Foreign Patents, patents in process, and are protected by trade secret 
 * or copyright law. Dissemination of this information or reproduction of this 
 * material is strictly forbidden unless prior written permission is obtained
 * from SecureFlag Limited.
 */

const { Editor } = toastui;
var codeSyntaxHightlight = Editor.plugin.codeSyntaxHighlight;
var colorSyntax = Editor.plugin.colorSyntax;
var table = Editor.plugin.tableMergedCell;

Number.isInteger = Number.isInteger || function(value) {
	return typeof value === 'number' && 
	isFinite(value) && 
	Math.floor(value) === value;
};
Array.prototype.remove = function(from, to) {
	var rest = this.slice((to || from) + 1 || this.length);
	this.length = from < 0 ? this.length + from : from;
	return this.push.apply(this, rest);
};
String.prototype.trim = function () {
	return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '');
};
String.prototype.replaceAll = function(search, replacement) {
	var target = this;
	return target.replace(new RegExp(search, 'g'), replacement);
};
String.prototype.hashCode = function() {
	var hash = 0, i, chr;
	if (this.length === 0) return hash;
	for (i = 0; i < this.length; i++) {
		chr   = this.charCodeAt(i);
		hash  = ((hash << 5) - hash) + chr;
	}
	return hash;
};
function autoplayMdVideo(selector){
	$(selector+' .mdvideo video').each(function(){
		this.autoplay = true;
		this.controls = true;
		this.load();    
	});
}
Object.size = function(obj) {
	var size = 0, key;
	for (key in obj) {
		if (obj.hasOwnProperty(key)) size++;
	}
	return size;
};
function isArray(what) {
    return Object.prototype.toString.call(what) === '[object Array]';
}
function getSum(total, num) {
	return total + num;
}
function toTitleCase(str)
{
	return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}
function htmlEncode(value){
	return $('<div/>').text(value).html();
}    
function deepCopy (arr) {
	var out = [];
	for (var i = 0, len = arr.length; i < len; i++) {
		var item = arr[i];
		var obj = {};
		for (var k in item) {
			obj[k] = item[k];
		}
		out.push(obj);
	}
	return out;
}
function cloneObj(obj){
	return JSON.parse(JSON.stringify(obj))
}
function replaceArrayContent(obj1, obj2){
	obj1.remove(0,(obj1.length-1));
	for(var i in obj2){
		obj1.push(obj2[i]);
	}
}
function replaceObjectContent(obj1, obj2){
	for (var key in obj1){
		if (obj1.hasOwnProperty(key)){
			delete obj1[key];
		}
	}
	for(var i in obj2){
		obj1[i] = obj2[i]
	}
}
jQuery.extend({
	deepclone: function(objThing) {

		if ( jQuery.isArray(objThing) ) {
			return jQuery.makeArray( jQuery.deepclone($(objThing)) );
		}
		return jQuery.extend(true, {}, objThing);
	},
});
function splitValue(value, index) {
	return (value.substring(0, index) + "," + value.substring(index)).split(',');
}
_st = function(fRef, mDelay) {
	if(typeof fRef == "function") {
		var argu = Array.prototype.slice.call(arguments,2);
		var f = (function(){ fRef.apply(null, argu); });
		return setTimeout(f, mDelay);
	}
	try{
		return window.setTimeout(fRef, mDelay);
	}
	catch(err){

	}
}
PNotify.prototype.options.stack.firstpos1 = 80; // or whatever pixel value you want.

var sf = angular.module('sfNg',['nya.bootstrap.select','jlareau.pnotify','ngRoute','ui.toggle','angular-table','chart.js','angular-notification-icons','angularSpinner','720kb.tooltips','ng-file-model','moment-picker','ngTagsInput']);


//register the interceptor as a service
var compareTo = function() {
	return {
		require: "ngModel",
		scope: {
			otherModelValue: "=compareTo"
		},
		link: function(scope, element, attributes, ngModel) {

			ngModel.$validators.compareTo = function(modelValue) {
				return modelValue == scope.otherModelValue;
			};

			scope.$watch("otherModelValue", function() {
				ngModel.$validate();
			});
		}
	};

};
sf.filter('capitalize', function() {
	return function(input) {
		return (!!input) ? input.charAt(0).toUpperCase() + input.substr(1).toLowerCase() : '';
	}
});
sf.filter('inParenthesis', function() {
	return function(input) {
		return (!!input) ? "(" + input + ")" : '';
	}
});
sf.filter('titleCase', function() {
	return function(input) {
		input = input || '';
		return input.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
	};
})

sf.directive("compareTo", compareTo);

sf.directive('complexPassword', function() {
	return {
		require: 'ngModel',
		link: function(scope, elm, attrs, ctrl) {
			ctrl.$parsers.unshift(function(password) {
				var hasUpperCase = /[A-Z]/.test(password);
				var hasLowerCase = /[a-z]/.test(password);
				var hasNumbers = /\d/.test(password);
				var hasNonalphas = /\W/.test(password);
				var characterGroupCount = hasUpperCase + hasLowerCase + hasNumbers + hasNonalphas;

				if ((password.length >= 8) && (characterGroupCount >= 3)) {
					ctrl.$setValidity('complexity', true);
					return password;
				}
				else {
					ctrl.$setValidity('complexity', false);
					return undefined;
				}

			});
		}
	}
});
sf.service('server',function($http,$timeout,$rootScope,notificationService,$interval){ 

	var $this = this; 

	this.supportedAwsRegions = [];
	this.definedGateways = [];
	this.definedGatewaysRegions = [];

	$rootScope.hashCode = function(string) {
		var hash = 0, i, chr;
		if (string.length === 0) return hash;
		for (i = 0; i < string.length; i++) {
			chr   = string.charCodeAt(i);
			hash  = ((hash << 5) - hash) + chr;
		}
		return hash;
	};

	$rootScope.getRandom = function(){
		return Math.floor(100000 + Math.random() * 900000);
	}

	this.loadVulnKBTechnology = function(uuid,technology){
		$('.waitLoader').show();
		var obj = {};
		obj.action = 'getKBItem';
		obj.uuid = uuid;
		obj.technology = technology;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$http(req).then(function successCallback(response) {
			$rootScope.$broadcast('vulnKBLoaded:updated',response.data);
			$('.waitLoader').hide();
		}, function errorCallback(response) {
			console.log('ajax error');
		});
	}
	
	this.loadVulnKB = function(uuid){
		$('.waitLoader').show();
		var obj = {};
		obj.action = 'getKBItem';
		obj.uuid = uuid;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$http(req).then(function successCallback(response) {
			$rootScope.$broadcast('vulnKBLoaded:updated',response.data);
			$('.waitLoader').hide();
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	this.loadStackKB = function(uuid){
		$('.waitLoader').show();

		var obj = {};
		obj.action = 'getStackItem';
		obj.uuid = uuid;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$http(req).then(function successCallback(response) {
			$rootScope.$broadcast('stackKBLoaded:updated',response.data);
			$('.waitLoader').hide();
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}

	this.updateTechnology = function(tmpTech){
		var obj ={};
		obj.action = 'updateTechnology';
		obj.obj = tmpTech;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('updateTechnology:updated',response.data);
			if(undefined == response.data.result || response.data.result!="error"){
				PNotify.removeAll();
				notificationService.success('Technology Stack KB item updated.');
			}
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	this.deleteTechnology = function(tmpTech){
		var obj ={};
		obj.action = 'deleteTechnology';
		obj.uuid = tmpTech.uuid;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('deleteTechnology:updated',response.data);
			if(response.data.result=="success"){
				PNotify.removeAll();
				notificationService.success('Technology Stack KB item deleted.');
			}
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	
	this.addFramework = function(name){
		var obj ={};
		obj.action = 'addFramework';
		obj.name = name;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('addFramework:updated',response.data);
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	this.removeFramework = function(name){
		var obj ={};
		obj.action = 'removeFramework';
		obj.name = name;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('removeFramework:updated',response.data);
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	this.getFrameworks = function(){
		var obj ={};
		obj.action = 'getFrameworks';
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('getFrameworks:updated',response.data);
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	
	this.addTechnology = function(tmpTech){
		var obj ={};
		obj.action = 'addTechnology';
		obj.obj = tmpTech;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('addTechnology:updated',response.data);
			if(undefined == response.data.result || response.data.result!="error"){
				PNotify.removeAll();
				notificationService.success('Technology Stack KB item added.');
			}
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}

	this.updateVulnerability = function(tmpVuln){
		var obj ={};
		obj.action = 'updateVulnerability';
		obj.obj = tmpVuln;		
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('updateVulnerability:updated',response.data);
			if(undefined == response.data.result || response.data.result!="error"){
				PNotify.removeAll();
				notificationService.success('Vulnerability KB item updated.');
			}
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	this.deleteVulnerability = function(tmpVuln){
		var obj ={};
		obj.action = 'deleteVulnerability';
		obj.uuid = tmpVuln.uuid;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('deleteVulnerability:updated',response.data);
			if(response.data.result=="success"){
				PNotify.removeAll();
				notificationService.success('Vulnerability KB item deleted.');
			}
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	this.addVulnerability = function(tmpVuln){
		var obj ={};
		obj.action = 'addVulnerability';
		obj.obj = tmpVuln;
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('addVulnerability:updated',response.data);
			if(undefined == response.data.result || response.data.result!="error"){
				PNotify.removeAll();
				notificationService.success('Vulnerability KB item added.');
			}
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});
	}
	
	this.getAllStacks = function(){

		var obj ={};
		obj.action = 'getAllStacks';

		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,	
		}
		$http(req).then(function successCallback(response) {
			$rootScope.$broadcast('stackKbs:updated',response.data);
		}, function errorCallback(response) {
			console.log('ajax error');
		});
	}


	this.addExercise = function(exercise){

		var obj = cloneObj(exercise);
		obj.action = 'addExercise';

		for(var i=0;i<obj.tags.length;i++){
			if (typeof obj.tags[i] === 'string' || obj.tags[i] instanceof String){
				continue;
			}
			else{
				obj.tags[i] = obj.tags[i].text;
			}
		}
		for(var j=0;j<obj.flags.length;j++){
			for(var k=0;k<obj.flags[j].flagList.length;k++){
				if(undefined!=obj.flags[j].flagList[k] && undefined!=obj.flags[j].flagList[k].selfCheck){
					for(var l in obj.flags[j].flagList[k].selfCheck.statusMapping){
						if (obj.flags[j].flagList[k].selfCheck.statusMapping.hasOwnProperty(l) && typeof obj.flags[j].flagList[k].selfCheck.statusMapping[l] === 'string' || obj.flags[j].flagList[k].selfCheck.statusMapping[l] instanceof String){
							continue;
						}
						else{
							if(undefined!=obj.flags[j].flagList[k].selfCheck.statusMapping[l].id)
								obj.flags[j].flagList[k].selfCheck.statusMapping[l] = obj.flags[j].flagList[k].selfCheck.statusMapping[l].id;
						}
					}
				}
			}
		}
		var req = {
				method: 'POST',
				url: '/handler',
				data: obj,
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			if(undefined == response.data.result || response.data.result!="error"){
				PNotify.removeAll();
				notificationService.success('Exercise added.');
				$rootScope.$broadcast('exerciseAdded:updated',response.data);
			}
			else{
				PNotify.removeAll();
				notificationService.notice('Updated failed, please try again.');
			}

		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});

	};

	$rootScope.ctoken = "";

	this.getCToken = function(){
		var msg = {};
		msg.action = 'getUserCToken';

		var req = {
				method: 'POST',
				url: '/handler',
				data: msg,
		}
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.ctoken = response.data.ctoken;
			$this.getInitialData();
		}, function errorCallback(response) {
			console.log('ajax error');
			$('.waitLoader').hide();
		});
	}
	this.getCToken();

	this.getInitialData = function(){  
		$this.getAvailableExercises();	
		$this.getAllKbs();
		$this.getAllStacks();
		$this.getFrameworks();
		initialData = true;
	}

	this.updateExercise = function(exercise){
		var obj = cloneObj(exercise);
		obj.action = 'updateExercise';
		for(var i=0;i<obj.tags.length;i++){
			if (typeof obj.tags[i] === 'string' || obj.tags[i] instanceof String){
				continue;
			}
			else{
				obj.tags[i] = obj.tags[i].text;
			}
		}
		for(var j=0;j<obj.flags.length;j++){
			for(var k=0;k<obj.flags[j].flagList.length;k++){
				if(undefined!=obj.flags[j].flagList[k] && undefined!=obj.flags[j].flagList[k].selfCheck){
					for(var l in obj.flags[j].flagList[k].selfCheck.statusMapping){
						if (obj.flags[j].flagList[k].selfCheck.statusMapping.hasOwnProperty(l) && typeof obj.flags[j].flagList[k].selfCheck.statusMapping[l] === 'string' || obj.flags[j].flagList[k].selfCheck.statusMapping[l] instanceof String){
							continue;
						}
						else{
							if(undefined!=obj.flags[j].flagList[k].selfCheck.statusMapping[l].id)
								obj.flags[j].flagList[k].selfCheck.statusMapping[l] = obj.flags[j].flagList[k].selfCheck.statusMapping[l].id;
						}
					}
				}
			}
		}
		var req = {
			method: 'POST',
			url: '/handler',
			data: obj,
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			if(undefined == response.data.result || response.data.result!="error"){
				PNotify.removeAll();
				notificationService.success('Exercise updated.');
				$rootScope.$broadcast('exerciseUpdated:updated',response.data);
			}
			else{
				PNotify.removeAll();
				notificationService.notice('Updated failed, please try again.');
			}
		}, function errorCallback(response) {
			$('.waitLoader').hide();
			console.log('ajax error');
		});

	}

	this.getAllKbs  = function(){

		var msg = {};
		msg.action = 'getAllKbs';

		var req = {
				method: 'POST',
				url: '/handler',
				data: msg
		}
		$http(req).then(function successCallback(response) {
			$rootScope.$broadcast('vulnerabilityKbs:updated',response.data);
		}, function errorCallback(response) {
			console.log('ajax error');
		});

	}    

	this.getExerciseDetails = function(uuid){

		var msg = {};
		msg.action = 'getExerciseDetails';
		msg.uuid = uuid;

		var req = {
				method: 'POST',
				url: '/handler',
				data: msg
		}
		$('.waitLoader').show();
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.$broadcast('exerciseDetails:updated',response.data);
		}, function errorCallback(response) {
			console.log('ajax error');
			$('.waitLoader').hide();
		});

	}



	this.getAvailableExercises = function(){

		var msg = {};
		msg.action = 'getExercises';

		var req = {
				method: 'POST',
				url: '/handler',
				data: msg,
		}
		$http(req).then(function successCallback(response) {
			$rootScope.$broadcast('availableExercises:updated',response.data);
		}, function errorCallback(response) {
			console.log('ajax error');
			$('.waitLoader').hide();
		});

	}
})
sf.controller('navigation',['$rootScope','$scope','server','$timeout','$http','$location',function($rootScope,$scope,server,$timeout,$http,$location){
	$scope.user = server.user;



	
	$scope.goTo = function(link){
		$location.path(link.replace("#",""), false);
	}


	$rootScope.$on('$locationChangeSuccess', function(event, newUrl, oldUrl){
		if(newUrl.indexOf('d2h-')>-1){
			return;
		}
		var target = newUrl.substr(newUrl.indexOf("#")).replace("#","").replace("/","");
		target = target.split("/")
		switch(target[0]){       

		
		case "available-exercises":
			if(target[1]=="new"){
				return;
			}
			if(target[3]=="flags" || target[3] == "info"){
				return;
			}
			if(target[1]=="details"){
				$rootScope.visibility.users = false;
				$rootScope.visibility.settings = false;
				$rootScope.visibility.downloads = false;
				$rootScope.visibility.grants = false;
				$rootScope.visibility.uploads = false;
				$rootScope.visibility.paths = false;
				$rootScope.visibility.kb = false;
				$rootScope.visibility.grants = false;
				$rootScope.visibility.uploads = false;
				$rootScope.visibility.availableExercises = true;
				if(undefined!=target[2] && ""!=target[2] && (undefined==$rootScope.ctoken || ""==$rootScope.ctoken)){
					getExDetails(target[2]);
				}
			}
			else{
				$rootScope.visibility.users = false;
				$rootScope.visibility.paths = false;
				$rootScope.visibility.grants = false;
				$rootScope.visibility.uploads = false;
				$rootScope.visibility.downloads = false;
				$rootScope.visibility.settings = false;
				$rootScope.visibility.kb = false;
				$rootScope.visibility.grants = false;
				$rootScope.visibility.uploads = false;
				$rootScope.visibility.availableExercises = true;
				$rootScope.showExerciseList = true;
				$rootScope.showExerciseDetails = false;
			}
			$(window).scrollTop(0);
			break;

		case "kb":
			$rootScope.visibility.kb = true;
			$rootScope.visibility.users = false;
			$rootScope.visibility.downloads = false;
			$rootScope.visibility.settings = false;
			$rootScope.visibility.paths = false;
			$rootScope.visibility.grants = false;
			$rootScope.visibility.uploads = false;
			$rootScope.visibility.availableExercises = false;
			$(window).scrollTop(0);
			break;
		default:{
			$rootScope.visibility.paths = false;
			$rootScope.visibility.users = false;
			$rootScope.visibility.downloads = false;
			$rootScope.visibility.settings = false;
			$rootScope.visibility.kb = false;
			$rootScope.visibility.grants = false;
			$rootScope.visibility.uploads = false;
			$rootScope.visibility.availableExercises = true;
			$(window).scrollTop(0);
			break;
		}

		}        

	});

	function getExDetails(uuid){

		var msg = {};
		msg.action = 'getUserCToken';

		var req = {
				method: 'POST',
				url: '/handler',
				data: msg,
		}
		$http(req).then(function successCallback(response) {
			$('.waitLoader').hide();
			$rootScope.ctoken = response.data.ctoken;
			server.getExerciseDetails(uuid);
		}, function errorCallback(response) {
			console.log('ajax error');
		});


	}

	$rootScope.visibility = {}
	$rootScope.visibility.availableExercises = true;
	$rootScope.visibility.kb = false;

}])
sf.factory('xhrInterceptor', ['$q','$rootScope', function($q, $rootScope) {
	return {
		'request': function(config) {
			if(config.url == "/handler" && config.data.action !=undefined && config.data.action != "getUserCToken")
				config.data.ctoken = $rootScope.ctoken;
			return config;
		},
		'response': function(response) {
			if(undefined!=response && undefined!=response.data){
				try{
					if(response.data.indexOf('PLATFORM')>0){
						document.location = "/index.html";
					}
				}catch(err){}
			}
			return response;
		}
	};
}]);
sf.run(['$route', '$rootScope', '$location', function ($route, $rootScope, $location) {
	var original = $location.path;
	$location.path = function (path, reload) {
		if (reload === false) {
			var lastRoute = $route.current;
			var un = $rootScope.$on('$locationChangeSuccess', function () {
				$route.current = lastRoute;
				un();
			});
		}
		return original.apply($location, [path]);
	};
}])
sf.config(['$httpProvider', function($httpProvider) {  
	$httpProvider.interceptors.push('xhrInterceptor');
}]);
sf.controller('kb',['$scope','server','$filter','$rootScope',function($scope,server,$filter,$rootScope){
	$scope.saveFlow = false;
	$scope.filteredKBsList = []; 
	$scope.selectedKBRow = -1;
	$scope.kbstableconfig = {
			itemsPerPage: 20,
			fillLastPage: false
	}
	
	$rootScope.exerciseFrameworksList = [];
	$scope.newFrameworkName = "";
	$scope.addFramework = function(){
		if($scope.newFrameworkName != "")
			server.addFramework($scope.newFrameworkName);
	}
	$scope.removeFramework = function(name){
		server.removeFramework(name);
	}
	$scope.$on('removeFramework:updated', function(event,data) {
		server.getFrameworks();
	});
	$scope.$on('addFramework:updated', function(event,data) {
		server.getFrameworks();
	});
	$scope.$on('getFrameworks:updated', function(event,data) {
		$rootScope.exerciseFrameworksObjs = data;
		$rootScope.exerciseFrameworksList = [];
		for(var i = 0;i<data.length;i++){
			$rootScope.exerciseFrameworksList.push(data[i].name);
		}
	});
	

	$rootScope.kbItems = []
	$rootScope.stackItems = []
	$scope.openVulnKB = function(item){
		$scope.vulnSaveFlow = false;

		for(var j=0; j<$rootScope.kbItems.length; j++){
			if($rootScope.kbItems[j].uuid == item.uuid && undefined != $rootScope.kbItems[j].md && undefined != $rootScope.kbItems[j].text && $rootScope.kbItems[j].md.text != ""){
				document.querySelector('#kbViewMD').innerHTML = '';
				var cMd = $rootScope.kbItems[j].md.text+"\n";
				if($rootScope.kbItems[j].kbMapping!=undefined){
					for(var i=0;i<Object.keys($rootScope.kbItems[j].kbMapping).length;i++){
						var tmpInner = $rootScope.kbItems[j].kbMapping[Object.keys($rootScope.kbItems[j].kbMapping)[i]]
						cMd += "\n***\n# "+tmpInner.technology+" #\n"+tmpInner.md.text+"\n";
					}
				}
				var editor = new toastui.Editor.factory({
					el: document.querySelector('#kbViewMD'),
					viewer: true,
					usageStatistics:false,
					height: '500px',
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					initialValue: ''
				});
				editor.setMarkdown(cMd);
				autoplayMdVideo('#kbViewMD');
				$('#kbViewModal').find('a').each(function() {
					if(this.href==undefined || this.href=="" || this.href.indexOf('#')==0)
						return;
					var a = new RegExp('/' + window.location.host + '/');
					if(!a.test(this.href)) {
						$(this).click(function(event) {
							event.preventDefault();
							event.stopPropagation();
							window.open(this.href, '_blank');
						});
					}
				});
				$('#kbViewModal').modal('show');
				var videos = document.getElementsByTagName('video')
				for(var v=0;v<videos.length;v++){
					videos[v].autoplay = true;
					videos[v].load();
				}
				return;
			}
		}
		server.loadVulnKB(item.uuid);
	}
	$scope.$on('vulnKBLoaded:updated', function(event,data) {

		if($rootScope.visibility.kb){



			if(!$scope.vulnSaveFlow){
				var cMd = data.md.text+"\n";
				if(data.kbMapping!=undefined){
					for(var i=0;i<Object.keys(data.kbMapping).length;i++){
						var tmpInner = data.kbMapping[Object.keys(data.kbMapping)[i]]
						cMd += "\n***\n# "+tmpInner.technology+" #\n"+tmpInner.md.text+"\n";
					}
				}
				document.querySelector('#kbViewMD').innerHTML = '';
				var editor = new toastui.Editor.factory({
					el: document.querySelector('#kbViewMD'),
					viewer: true,
					usageStatistics:false,
					height: '500px',
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					initialValue: ''
				});
				editor.setMarkdown(cMd);
				$('#kbViewModal').modal('show');
				autoplayMdVideo('#kbViewMD');
			}
			else {
				document.querySelector('#vulnEditorMD').innerHTML = '';
				$scope.tmpVuln.md = {}
				$scope.tmpVuln.md.text = data.md.text;
				var vulnEditor = new toastui.Editor({
					el: document.querySelector('#vulnEditorMD'),
					usageStatistics:false,
					height: '340px',
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					initialEditType: 'markdown',
					hideModeSwitch: true,
					initialValue: $scope.tmpVuln.md.text,
					events: {
						change: function() {
							$scope.tmpVuln.md.text = vulnEditor.getMarkdown();
						},
					}
				});
			}

			var kbFound = false;
			for(var j=0; j<$rootScope.kbItems.length; j++){
				if($rootScope.kbItems[j].uuid == data.uuid){
					$rootScope.kbItems[j] = data;
					kbFound = true;
					break;
				}
			}
			if(!kbFound){
				$rootScope.kbItems.push(data)
			}



		}
	})


	$scope.tmpTech = {};
	$scope.tmpTech.technology = "";
	$scope.tmpTech.variant = "";
	$scope.tmpTech.imageUrl = "";
	$scope.tmpTech.md = {};
	$scope.tmpTech.md.text = "";
	$scope.tmpVuln = {}
	$scope.tmpVuln.vulnerability = "";
	$scope.tmpVuln.isAgnostic = false;
	$scope.tmpVuln.kbMapping = {};
	$scope.tmpVulnMappings = [];
	$scope.tmpVuln.category = "";
	$scope.tmpVuln.technology = "";
	$scope.tmpVuln.md = {};
	$scope.tmpVuln.md.text = "";

	$scope.vulnerabilityCategories = ["Cross-Site Scripting","SQL Injection","XML Injection","Unsafe Deserialization","Cross-Site Request Forgery","Path Traversal","Use of Dangerous Function","Hardcoded Secrets","Sensitive Information Exposure","Inadequate Input Validation","Broken Cryptography","Open Redirect","Command Injection","Broken Authentication","Broken Session Management","Broken Authorization","Unrestricted File Upload","Server-Side Template Injection"]

	$scope.updateTmpVulnByTech = function(){
		$rootScope.nonAgnosticKbItems = $filter("filter")($rootScope.kbItems, { technology: $scope.tmpVulnMapping.technology});
	}
	$scope.deleteTmpVulnMapping = function(item){
		for(var i=0; i<$scope.tmpVulnMappings.length;i++){
			if($scope.tmpVulnMappings[i].technology == item.technology){
				$scope.tmpVulnMappings.remove(i,i);
				return;
			}
		}
	};
	$scope.addTmpVulnMapping = function(){
		var a = { technology: $scope.tmpVulnMapping.technology, vulnerability: $scope.tmpVulnMapping.vulnerability}
		for(var i=0; i<$scope.tmpVulnMappings.length;i++){
			if($scope.tmpVulnMappings[i].technology == $scope.tmpVulnMapping.technology)
				return;
		}
		$scope.tmpVulnMappings.push(a);
	};
	
	$scope.addVulnerabilityModal = function(){
		$scope.vulnSaveFlow = false;
		$scope.tmpVuln = {}
		$scope.tmpVuln.vulnerability = "";
		$scope.tmpVuln.category = "";
		$scope.tmpVuln.technology = "";
		$scope.tmpVuln.isAgnostic = false;
		$scope.tmpVuln.kbMapping = {};
		$scope.tmpVulnMappings = [];
		$scope.tmpVuln.md = {};
		$scope.tmpVuln.md.text = "";
		document.querySelector('#vulnEditorMD').innerHTML = '';
		var vulnEditor = new toastui.Editor({
			el: document.querySelector('#vulnEditorMD'),
			usageStatistics:false,
			height: '340px',
			plugins: [ codeSyntaxHightlight, table, colorSyntax ],
			initialEditType: 'markdown',
			hideModeSwitch: true,
			initialValue: $scope.tmpVuln.md.text,
			events: {
				change: function() {
					$scope.tmpVuln.md.text = vulnEditor.getMarkdown();
				},
			}
		});
		$('#addVulnerabilityModal').modal('show');

	}
	$scope.addVulnerability = function(){
		$scope.tmpVuln.kbMapping = {};
		if($scope.tmpVuln.isAgnostic){
			for(var i=0;i<$scope.tmpVulnMappings.length;i++){
				$scope.tmpVuln.kbMapping[$scope.tmpVulnMappings[i].technology] = $scope.tmpVulnMappings[i].vulnerability;
			}
		}
		$scope.tmpVuln.lastUpdate = new Date();
		server.addVulnerability($scope.tmpVuln);
	}
	$scope.editVulnerabilityModal = function(item){
		$scope.vulnSaveFlow = true;
		if(undefined!=item.fromHub && item.fromHub == true){
			server.loadVulnKB(item.uuid);
		}
		else{
			$scope.tmpVuln.md = {};
			$scope.tmpVuln.md.text = item.md.text;
			document.querySelector('#vulnEditorMD').innerHTML = '';
			var vulnEditor = new toastui.Editor({
				el: document.querySelector('#vulnEditorMD'),
				usageStatistics:false,
				height: '340px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				initialEditType: 'markdown',
				hideModeSwitch: true,
				initialValue: $scope.tmpVuln.md.text,
				events: {
					change: function() {
						$scope.tmpVuln.md.text = vulnEditor.getMarkdown();
					},
				}
			});
		}
		$scope.tmpVuln.id = item.id;
		$scope.tmpVuln.uuid = item.uuid;
		$scope.tmpVuln.isAgnostic = item.isAgnostic || false;
		$scope.tmpVuln.vulnerability = item.vulnerability;
		$scope.tmpVuln.category = item.category;
		$scope.tmpVuln.technology = item.technology;
		$scope.tmpVuln.kbMapping = item.kbMapping || {};
		$scope.tmpVulnMappings = [];
		var keys = Object.keys($scope.tmpVuln.kbMapping);
		for(var j=0; j<keys.length;j++){
			var a = { technology: keys[j], vulnerability: $scope.tmpVuln.kbMapping[keys[j]]};
			$scope.tmpVulnMappings.push(a);
		}
		$('#addVulnerabilityModal').modal('show');
	}
	$scope.$on('updateVulnerability:updated', function(event,data) {
		$scope.tmpVuln = {}
		$scope.tmpVuln.vulnerability = "";
		$scope.tmpVuln.category = "";
		$scope.tmpVuln.technology = "";
		$scope.tmpVuln.isAgnostic = false;
		$scope.tmpVuln.md = {};
		$scope.tmpVuln.kbMapping = {};
		$scope.tmpVulnMappings = [];
		$scope.tmpVuln.md.text = "";
		$('#addVulnerabilityModal').modal('hide');
		server.getAllKbs();
	});
	$scope.$on('addVulnerability:updated', function(event,data) {
		$scope.tmpVuln = {}
		$scope.tmpVuln.vulnerability = "";
		$scope.tmpVuln.category = "";
		$scope.tmpVuln.technology = "";
		$scope.tmpVuln.isAgnostic = false;
		$scope.tmpVuln.md = {};
		$scope.tmpVuln.kbMapping = {};
		$scope.tmpVulnMappings = [];
		$scope.tmpVuln.md.text = "";
		$('#addVulnerabilityModal').modal('hide');
		server.getAllKbs();
	});
	$scope.$on('deleteVulnerability:updated', function(event,data) {
		$('#deleteVulnerabilityModal').modal('hide');
		server.getAllKbs();
	});
	$scope.$on('updateTechnology:updated', function(event,data) {
		$scope.tmpTech = {};
		$scope.tmpTech.technology = "";
		$scope.tmpTech.variant = "";
		$scope.tmpTech.imageUrl = "";
		$scope.tmpTech.md = {};
		$scope.tmpTech.md.text = "";
		$('#addStackModal').modal('hide');
		server.getAllStacks();
	});
	$scope.$on('addTechnology:updated', function(event,data) {
		$scope.tmpTech = {};
		$scope.tmpTech.technology = "";
		$scope.tmpTech.variant = "";
		$scope.tmpTech.imageUrl = "";
		$scope.tmpTech.md = {};
		$scope.tmpTech.md.text = "";
		$('#addStackModal').modal('hide');
		server.getAllStacks();
	});
	$scope.$on('deleteTechnology:updated', function(event,data) {
		$('#deleteTechnologyModal').modal('hide');
		server.getAllStacks();
	});

	$scope.updateVulnerability = function(){
		$scope.tmpVuln.kbMapping = {};
		if($scope.tmpVuln.isAgnostic){
			for(var i=0;i<$scope.tmpVulnMappings.length;i++){
				$scope.tmpVuln.kbMapping[$scope.tmpVulnMappings[i].technology] = $scope.tmpVulnMappings[i].vulnerability;
			}
		}
		$scope.tmpVuln.lastUpdate = new Date();
		server.updateVulnerability($scope.tmpVuln);
	}
	$scope.deleteVulnerabilityModal = function(item){
		$scope.tmpVulnDeleteItem = item;
		$('#deleteVulnerabilityModal').modal('show');
	}
	$scope.deleteVulnerability = function(){
		server.deleteVulnerability($scope.tmpVulnDeleteItem);
	}
	$scope.addTechnology = function(){
		$scope.tmpTech.lastUpdate = new Date();
		server.addTechnology($scope.tmpTech);
	}
	$scope.deleteTechnology = function(){
		server.deleteTechnology($scope.tmpTechDeleteItem);
	}
	$scope.deleteTechnologyModal = function(item){
		$scope.tmpTechDeleteItem = item;
		$('#deleteTechnologyModal').modal('show');
	}
	$rootScope.getDateInCurrentTimezone = function(date,format){
		if(date==null)
			return "N/A"
			return moment(date).local().format(format);
	}

	$scope.updateTechnology = function(){
		$scope.tmpTech.lastUpdate = new Date();
		server.updateTechnology($scope.tmpTech);
	}
	$scope.editTechnologyModal = function(item){
		$scope.stackSaveFlow = true;
		$scope.tmpTech.id = item.id;
		$scope.tmpTech.uuid = item.uuid;
		$scope.tmpTech.imageUrl = item.imageUrl;
		$scope.tmpTech.variant = item.variant;
		$scope.tmpTech.technology = item.technology;
		if(undefined!=item.fromHub && item.fromHub == true){
			server.loadStackKB(item.uuid);
		}
		else{
			$scope.tmpTech.md = {}
			$scope.tmpTech.md.text = item.md.text;
			document.querySelector('#stackEditorMD').innerHTML = '';
			var technologyEditor = new toastui.Editor({
				el: document.querySelector('#stackEditorMD'),
				usageStatistics:false,
				height: '340px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				initialValue: $scope.tmpTech.md.text,
				initialEditType: 'markdown',
				hideModeSwitch: true,
				events: {
					change: function() {
						$scope.tmpTech.md.text = technologyEditor.getMarkdown();
					},
				}
			});
		}
		$('#addStackModal').modal('show');
	}


	$scope.addTechnologyModal = function(){
		$scope.stackSaveFlow = false;
		document.querySelector('#stackEditorMD').innerHTML = '';
		var technologyEditor = new toastui.Editor({
			el: document.querySelector('#stackEditorMD'),
			usageStatistics:false,
			height: '340px',
			plugins: [ codeSyntaxHightlight, table, colorSyntax ],
			initialEditType: 'markdown',
			hideModeSwitch: true,
			initialValue: "",
			events: {
				change: function() {
					$scope.tmpTech.md.text = technologyEditor.getMarkdown();
				},
			}
		});
		$('#addStackModal').modal('show');

	}

	$scope.openStackKB = function(item){
		$scope.stackSaveFlow = false;

		for(var j=0; j<$rootScope.stackItems.length; j++){
			if($rootScope.stackItems[j].uuid == item.uuid && undefined != $rootScope.stackItems[j].md && undefined != $rootScope.stackItems[j].md.text && $rootScope.stackItems[j].md.text != ""){
				document.querySelector('#stackViewMD').innerHTML = '';
				var editor = new toastui.Editor.factory({
					el: document.querySelector('#stackViewMD'),
					viewer: true,
					usageStatistics:false,
					height: '500px',
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					initialValue: $rootScope.stackItems[j].md.text
				});
				$('#stackViewModal').modal('show');
				autoplayMdVideo('#stackViewMD');
				return;
			}
		}
		server.loadStackKB(item.uuid);
	}
	$scope.$on('stackKBLoaded:updated', function(event,data) {
		if($rootScope.visibility.kb){
			if(!$scope.stackSaveFlow){
				document.querySelector('#stackViewMD').innerHTML = '';
				var editor = new toastui.Editor.factory({
					el: document.querySelector('#stackViewMD'),
					viewer: true,
					usageStatistics:false,
					height: '500px',
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					initialValue: data.md.text
				});
				$('#stackViewModal').modal('show');
				autoplayMdVideo('#stackViewMD');
			}
			else {
				$scope.tmpTech.md = {};
				$scope.tmpTech.md.text = data.md.text;
				document.querySelector('#stackEditorMD').innerHTML = '';
				var technologyEditor = new toastui.Editor({
					el: document.querySelector('#stackEditorMD'),
					usageStatistics:false,
					height: '340px',
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					initialValue: $scope.tmpTech.md.text,
					initialEditType: 'markdown',
					hideModeSwitch: true,
					events: {
						change: function() {
							$scope.tmpTech.md.text = technologyEditor.getMarkdown();
						},
					}
				});
			}

			var kbFound = false;
			for(var j=0; j<$rootScope.stackItems.length; j++){
				if($rootScope.stackItems[j].uuid == data.uuid){
					$rootScope.stackItems[j] = data;
					kbFound = true;
					break;
				}
			}
			if(!kbFound){
				$rootScope.stackItems.push(data)
			}

		}
	})
	$scope.updateFilteredList = function() {
		$scope.filteredKBsList = $filter("filter")($rootScope.kbItems, $scope.query);
	};
	$scope.updateStackFilteredList = function() {
		$scope.filteredStacksList = $filter("filter")($rootScope.stackItems, $scope.queryStack);
	};
	$rootScope.stackItems = [];
	$scope.filteredStacksList = []; 
	$scope.selectedStackRow = -1;
	$scope.stackstableconfig = {
			itemsPerPage: 20,
			fillLastPage: false
	}
	$scope.$on('stackKbs:updated', function(event,data) {
		$rootScope.stackItems = data;
		$rootScope.technologyList = [];
		for(var i=0;i<$rootScope.stackItems.length;i++){
			$rootScope.stackItems[i].lastUpdate = $rootScope.stackItems[i].lastUpdate.replaceAll(/\[.*\]/,'');
			if($rootScope.technologyList.indexOf($rootScope.stackItems[i].technology)<0)
				$rootScope.technologyList.push($rootScope.stackItems[i].technology)
		}
		$scope.updateStackFilteredList();
	});
	$scope.$on('vulnerabilityKbs:updated', function(event,data) {
		for(var i=0;i<data.length;i++){
			data[i].lastUpdate = data[i].lastUpdate.replaceAll(/\[.*\]/,'');
		}
		$rootScope.kbItems = data;
		$scope.updateFilteredList();
	});
}]);
sf.controller('availableExercises',['$scope','server','$rootScope','$location','$filter','notificationService',function($scope,server,$rootScope,$location,$filter,notificationService){

	$scope.selectedExercises = "";
	$scope.filteredAvailableExercisesList = [];
	$scope.user = server.user;
	$scope.masterAvailableExercisesList = [];
	$scope.availableRegions = [];
	$rootScope.showExerciseList = true;
	$rootScope.showExerciseDetails = false;
	$scope.supportedAwsRegions = server.supportedAwsRegions;
	$scope.definedGateways = server.definedGateways;
	$scope.definedGatewaysRegions = server.definedGatewaysRegions;

	$scope.newExerciseFlagList = true;
	$scope.saveFlow = false;
	$rootScope.vulnerabilityStatus = [{id:0, name:"Not Vulnerable"},{id:1, name:"Vulnerable"},{id:2, name:"Broken Functionality"},{id:4, name:"Not Addressed"},{id:3, name:"N/A"},{id:5,name:"Partially Remediated"}]

	var baseTags = ["category","curriculum","cve","cwe","framework","vulnerability","technology"];
	$scope.loadTags = function(query) {
		var search_term = query.toUpperCase();
		$scope.matchingTags = [];
		angular.forEach(baseTags, function(item) {
			if (item.toUpperCase().indexOf(search_term) >= 0)
				$scope.matchingTags.push(item);

		});

		return $scope.matchingTags;
	};

	$scope.qualityList = ["0","1","2","3","4"]

	$scope.getNameFromQualityId = function(id){
		switch(id){
		case '0':
			return "Hub Default";
		case '1':
			return "Hub Vetted";
		case '2':
			return "SF Default";
		case '3':
			return "SF Vetted";
		case '4':
			return "SF Custom";
		}
	}

	function initEmptyExercise(){

		$scope.tmpNewExercise = {}
		$scope.tmpNewExercise.image = {}
		$scope.tmpNewExercise.image.taskDefinitionName = "";
		$scope.tmpNewExercise.image.containerName = "";
		$scope.tmpNewExercise.image.imageUrl = "";
		$scope.tmpNewExercise.image.hardMemory = "";
		$scope.tmpNewExercise.image.softMemory = "";
		$scope.tmpNewExercise.solution = { text : ""};
		$scope.tmpNewExercise.information = { text : ""};
		$scope.tmpNewExercise.ignoreDefaultStack = false;
		$scope.tmpNewExercise.difficulty = "";
		$scope.tmpNewExercise.status = "0";
		$scope.tmpNewExercise.technology = "";
		$scope.tmpNewExercise.framework = "";
		$scope.tmpNewExercise.variant = "";
		$scope.tmpNewExercise.duration = "";
		$scope.tmpNewExercise.description = "";
		$scope.tmpNewExercise.flags = []
		$scope.tmpNewExercise.subtitle = "";
		$scope.tmpNewExercise.title = "";
		$scope.tmpNewExercise.author = ""; 
		$scope.tmpNewExercise.exerciseType = "BOTH"; 
		$scope.tmpNewExercise.tags = [];
		$scope.tmpNewExercise.quality = 0;
		$scope.tmpNewExercise.tmpAwsAccountId = "";
		$scope.tmpNewExercise.trophyName = ""; 
		$scope.tmpNewExercise.authorizedUsers = [];
		$scope.tmpNewExercise.privateExercise = false;

		$scope.tmpFlag = {};
		$scope.tmpFlag.title = "";
		$scope.tmpFlag.selfCheck = { name: "", messageMappings: {}, statusMapping: {}};
		$scope.tmpFlag.selfCheckAvailable = false;
		$scope.tmpFlag.hint = { md: { text : ""}, type: "", scoreReducePercentage: ""};
		$scope.tmpFlag.hintAvailable  = false;
		$scope.tmpFlag.maxScore = 0;
		$scope.tmpFlag.optional = "";
		$scope.tmpFlag.type = "";
		$scope.tmpFlag.md = {};
		$scope.tmpFlag.md.text = "";
		$scope.tmpFlag.KBItem = "";


		$scope.tmpCheckerStatus = "";
		$scope.tmpCheckerMapping = "";
		$scope.tmpCheckerMessage = "";
		$scope.tmpSelfCheckMappings = [];

	}
	initEmptyExercise()
	$scope.tmpExerciseImage = {};

	var defaultMessages = {
			"Not Vulnerable":'<span style="color:#3c763d">**Congratulations!**</span> Your answer is correct. The vulnerability has been fixed!',
			'Not Addressed':'<span style="color:#e11d21">**Oops!** </span> The issue has not been addressed. Please follow the instructions.',
			'Vulnerable':'<span style="color:#e11d21">**Oops!** </span> Your answer is not correct. Please try again.',
			'Broken Functionality':'<span style="color:#e11d21">**Oops!** </span>  The functionality is not working anymore, fix it or restore the application\'s source code to its initial state.',
			'Partially Remediated':'<span style="color:#efab53">**Oops!** </span> You are getting closer! The issue has been partially remediated.'
	}

	$scope.updateDefaultMessage = function(){
		var res = defaultMessages[$scope.tmpCheckerMapping.name];
		if(undefined!=res){
			$scope.tmpCheckerMessage =  res;
			checkerMessageEditor.setMarkdown($scope.tmpCheckerMessage)
		}
	}
	var checkerMessageEditor;
	$scope.addTmpSelfCheckMapping = function(){

		for(var i in $scope.tmpSelfCheckMappings){
			if($scope.tmpSelfCheckMappings[i].status ==  $scope.tmpCheckerStatus){
				notificationService.notice("There is already a mapping with the same Self-Check status.")
				return;
			}
		}
		var obj = {};
		obj.status = $scope.tmpCheckerStatus;
		obj.mapping = $scope.tmpCheckerMapping
		obj.message = $scope.tmpCheckerMessage;
		$scope.tmpSelfCheckMappings.push(obj);
		$scope.tmpCheckerStatus = "";
		$scope.tmpCheckerMapping = "";
		$scope.tmpCheckerMessage = "";
		document.querySelector('#tmpCheckerMessage').innerHTML = "";
		checkerMessageEditor = new toastui.Editor({
			el: document.querySelector('#tmpCheckerMessage'),
			height: '150px',
			plugins: [ codeSyntaxHightlight, table, colorSyntax ],
			usageStatistics:false,
			initialEditType: 'markdown',
			hideModeSwitch: true,
			initialValue: "",
			events: {
				change: function() {
					$scope.tmpCheckerMessage = checkerMessageEditor.getMarkdown();
				},
			}
		}); 

	};

	$scope.deleteTmpSelfCheckMapping = function(item){
		$scope.tmpSelfCheckMappings = $scope.tmpSelfCheckMappings.filter(function(mapping, index, arr){
			return !(mapping.status == item.status && mapping.id == item.id)
		});
	};

	$rootScope.loadMarkdown = function(id,text){
		window.setTimeout(function(){
			document.querySelector('#'+id).innerHTML = "";
			var editor = new toastui.Editor.factory({
				el: document.querySelector('#'+id),
				height: '150px',
				usageStatistics:false,
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				initialValue: text,
				viewer:true
			}); 
			autoplayMdVideo('#'+id);
		},150);
	}


	$scope.$on('exerciseDefaultScoreUpdated:updated', function(event,data) {
		server.getExerciseDetails($rootScope.exerciseDetails.uuid);
	});

	$scope.enableAutomatedScoringForExercise = function(id){
		server.updateAutomatedScoringForExercise(id,0)
	}

	$scope.disableAutomatedScoringExercise = function(id){
		server.updateAutomatedScoringForExercise(id,2)
	}

	$rootScope.exerciseStatusList = ["AVAILABLE","COMING SOON","INACTIVE"]
	$rootScope.difficultyLevelList = ["Easy","Moderate","Hard"];
	$rootScope.technologyList = [];
	$rootScope.exerciseTypes = ["TRAINING","CHALLENGE","BOTH"]
	$rootScope.flagTypes = ["REMEDIATION","EXPLOITATION","SECURE CODING","OTHER"]
	$rootScope.variantList = [];


	$scope.updateDefaultStackInfoMD = function(){

		if(undefined!=$scope.tmpNewExercise.technology && $scope.tmpNewExercise.technology != ""){
			for(var i in $rootScope.stackItems){
				if($rootScope.stackItems[i].technology == $scope.tmpNewExercise.technology){
					server.loadStackKB($rootScope.stackItems[i].uuid);
				}
			}
			$rootScope.variantList = [];
			$rootScope.variantList.push("Default")
			for(var i in $rootScope.stackItems){
				if($rootScope.stackItems[i].technology == $scope.tmpNewExercise.technology && $rootScope.stackItems[i].variant != undefined && $rootScope.variantList.indexOf($rootScope.stackItems[i].variant)==-1)
					$rootScope.variantList.push($rootScope.stackItems[i].variant)
			}
		}
	}

	$scope.updateStackInfoAndVariant = function(){
		if(undefined!=$scope.tmpNewExercise.technology && $scope.tmpNewExercise.technology != ""){
			for(var i in $rootScope.stackItems){
				if($rootScope.stackItems[i].technology == $scope.tmpNewExercise.technology){
					if(($scope.tmpNewExercise.variant == "Default" && undefined == $rootScope.stackItems[i].variant) || ($rootScope.stackItems[i].variant == $scope.tmpNewExercise.variant)){
						server.loadStackKB($rootScope.stackItems[i].uuid);
						return;
					}
				}
			}
		}
	}
	$scope.$on('stackKBLoaded:updated', function(event,data) {

		if($rootScope.visibility.availableExercises){
	
			$scope.tmpNewExercise.stack = data;

			if($scope.saveFlow || !$rootScope.showExerciseDetails){
				document.querySelector('#EDStackMDViewer').innerHTML = "";
				var editor = new toastui.Editor.factory({
					el: document.querySelector('#EDStackMDViewer'),
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					height: '405px',
					usageStatistics:false,
					viewer: true,
					initialValue: data.md.text
				});
				autoplayMdVideo('#EDStackMDViewer');
				

			}
			else{
				document.querySelector('#exerciseStackMD').innerHTML = "";
				var editor = new toastui.Editor.factory({
					el: document.querySelector('#exerciseStackMD'),
					plugins: [ codeSyntaxHightlight, table, colorSyntax ],
					height: '405px',
					usageStatistics:false,
					viewer: true,
					initialValue: data.md.text
				});
				autoplayMdVideo('#exerciseStackMD');		
			}

			var kbFound = false;
			for(var j=0; j<$rootScope.stackItems.length; j++){
				if($rootScope.stackItems[j].uuid == data.uuid){
					$rootScope.stackItems[j] = data;
					kbFound = true;
					break;
				}
			}
			if(!kbFound){
				$rootScope.stackItems.push(data)
			}
			
		}
	});
	$scope.showAddExerciseModal = function(){
		$scope.saveFlow = false;
		$scope.ignoreDefaultStack = false;
		document.querySelector('#solutionMDEditor').innerHTML = "";
		var solutionMDEditor = new toastui.Editor({
			el: document.querySelector('#solutionMDEditor'),
			plugins: [ codeSyntaxHightlight, table, colorSyntax ],
			height: '405px',
			usageStatistics:false,
			initialEditType: 'markdown',
			hideModeSwitch: true,
			initialValue: $scope.tmpNewExercise.solution.text,
			events: {
				change: function() {
					$scope.tmpNewExercise.solution.text = solutionMDEditor.getMarkdown();
				},
			}
		});
		document.querySelector('#EDInfoMDEditor').innerHTML = "";
		var infoMDEditor = new toastui.Editor({
			el: document.querySelector('#EDInfoMDEditor'),
			plugins: [ codeSyntaxHightlight, table, colorSyntax ],
			height: '300px',
			usageStatistics:false,
			initialEditType: 'markdown',
			hideModeSwitch: true,
			initialValue: "",
			events: {
				change: function() {
					$scope.tmpNewExercise.information.text = infoMDEditor.getMarkdown();
				},
			}
		});
		$('#addNewExerciseModal').modal('show');
	}

	$scope.tmpAwsAccountId = "";
	$scope.removeAuthorizedUser = function(s){
		if(undefined!=s && "" != s.username){
			for(var i=0;i<$scope.tmpNewExercise.authorizedUsers.length;i++){
				if($scope.tmpNewExercise.authorizedUsers[i].username == s.username){
					$scope.tmpNewExercise.authorizedUsers.remove(i,i);
					return;
				}
			}
		}
	}
	$scope.addAuthorizedUser = function(){
		if(undefined==$scope.tmpNewExercise.authorizedUsers)
			$scope.tmpNewExercise.authorizedUsers = [];
		if(undefined!=$scope.tmpAwsAccountId && "" != $scope.tmpAwsAccountId && $scope.tmpNewExercise.authorizedUsers.indexOf($scope.tmpAwsAccountId)<0){
			var user = {}
			user.user = $scope.tmpAwsAccountId+"";
			$scope.tmpNewExercise.authorizedUsers.push(user)
			$scope.tmpAwsAccountId = "";
		}
	}

	$scope.updateExercise = function(){

		if($scope.tmpNewExercise.solution.text == "") {
			PNotify.removeAll();
			notificationService.notice('Please provide exercise solution.');
			return;
		}
		if($scope.tmpNewExercise.information.text == "" && $scope.tmpNewExercise.ignoreDefaultStack == true){
			PNotify.removeAll();
			notificationService.notice('Please exercise info or choose default technology stack info.');
			return;
		}
		if($scope.tmpNewExercise.flags.length==0){
			PNotify.removeAll();
			notificationService.notice('Please define at list one exercise flag.');
			return;

		}
		if($scope.tmpNewExercise.difficulty == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s difficulty.');
			return;
		}
		if($scope.tmpNewExercise.technology == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s technology.');
			return;
		}
		if($scope.tmpNewExercise.duration == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s duration.');
			return;
		}
		if($scope.tmpNewExercise.author == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s author.');
			return;
		}
		if($scope.tmpNewExercise.description == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s description.');
			return;
		}
		if($scope.tmpNewExercise.subtitle == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s topics.');
			return;
		}
		if($scope.tmpNewExercise.title == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s title.');
			return;
		}
		if($scope.tmpNewExercise.trophyName == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide trophy\'s title.');
			return;
		}
	
		$scope.tmpNewExercise.lastUpdate = new Date();

		server.updateExercise($scope.tmpNewExercise);

	}


	$scope.addNewExercise = function(){

		if($scope.tmpNewExercise.solution.text == "") {
			PNotify.removeAll();
			notificationService.notice('Please provide exercise solution.');
			return;
		}
		if($scope.tmpNewExercise.information.text == "" && $scope.tmpNewExercise.ignoreDefaultStack == true){
			PNotify.removeAll();
			notificationService.notice('Please exercise info or choose default technology stack info.');
			return;
		}
		if($scope.tmpNewExercise.flags.length==0){
			PNotify.removeAll();
			notificationService.notice('Please define at list one exercise flag.');
			return;
		}
		if($scope.tmpNewExercise.difficulty == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s difficulty.');
			return;
		}
		if($scope.tmpNewExercise.technology == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s technology.');
			return;
		}
		if($scope.tmpNewExercise.duration == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s duration.');
			return;
		}
		if($scope.tmpNewExercise.author == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s author.');
			return;
		}
		if($scope.tmpNewExercise.description == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s description.');
			return;
		}
		if($scope.tmpNewExercise.subtitle == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s topics.');
			return;
		}
		if($scope.tmpNewExercise.title == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide exercise\'s title.');
			return;
		}
		if($scope.tmpNewExercise.trophyName == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide trophy\'s title.');
			return;
		}
		$scope.tmpNewExercise.lastUpdate = new Date();
		server.addExercise($scope.tmpNewExercise);
	}

	$scope.$on('exerciseRemoved:updated', function(event,data) {
		server.getAvailableExercises();
	});


	$scope.loadedExerciseFile = {}
	$scope.showLoadExerciseModal = function(){
		$('#addNewExerciseModal').modal('hide');
		$scope.loadedExerciseFile = null;
		$('#loadExerciseModal').modal('show');
	}
	
	//TODO
	$scope.editExercise = function(){
		try{
			$scope.saveFlow = true;

			$scope.tmpNewExercise.id = $rootScope.exerciseDetails.id;
			$scope.tmpNewExercise.uuid = $rootScope.exerciseDetails.uuid;
			$scope.tmpNewExercise.difficulty = $rootScope.exerciseDetails.difficulty;
			$scope.tmpNewExercise.status = "0";
			$scope.tmpNewExercise.technology = $rootScope.exerciseDetails.technology;
			$scope.tmpNewExercise.duration = $rootScope.exerciseDetails.duration;
			$scope.tmpNewExercise.description =$rootScope.exerciseDetails.description;
			$scope.tmpNewExercise.subtitle = $rootScope.exerciseDetails.subtitle;
			$scope.tmpNewExercise.exerciseType = "BOTH";
			$scope.tmpNewExercise.author = $rootScope.exerciseDetails.author;
			$scope.tmpNewExercise.title = $rootScope.exerciseDetails.title;
			$scope.tmpNewExercise.trophyName = $rootScope.exerciseDetails.trophyName;  
			$scope.tmpNewExercise.information = $rootScope.exerciseDetails.information;
			$scope.tmpNewExercise.ignoreDefaultStack = $rootScope.exerciseDetails.ignoreDefaultStack;
			$scope.tmpNewExercise.stack = $rootScope.exerciseDetails.stack;
			$scope.tmpNewExercise.tags = $rootScope.exerciseDetails.tags;
			$scope.tmpNewExercise.quality = 0;
			$scope.tmpNewExercise.image = $rootScope.exerciseDetails.image;
			$scope.tmpNewExercise.privateExercise = $rootScope.exerciseDetails.privateExercise
			$scope.tmpNewExercise.authorizedUsers = $rootScope.exerciseDetails.authorizedUsers;
			if(undefined==$scope.tmpNewExercise.authorizedUsers)
				$scope.tmpNewExercise.authorizedUsers= [];
			if(undefined==$scope.tmpNewExercise.privateExercise)
				$scope.tmpNewExercise.privateExercise= false;

			if(undefined!=$scope.tmpNewExercise.technology && $scope.tmpNewExercise.technology != ""){
				$rootScope.variantList = [];
				$rootScope.variantList.push("Default")
				for(var i in $rootScope.stackItems){
					if($rootScope.stackItems[i].technology == $scope.tmpNewExercise.technology && $rootScope.stackItems[i].variant != undefined && $rootScope.variantList.indexOf($rootScope.stackItems[i].variant)==-1)
						$rootScope.variantList.push($rootScope.stackItems[i].variant)
				}
			}
			$scope.tmpNewExercise.framework = $rootScope.exerciseDetails.framework;
			if($scope.tmpNewExercise.framework==undefined || $scope.tmpNewExercise.framework == "")
				$scope.tmpNewExercise.framework = "Default";
			
			$scope.tmpNewExercise.variant = $rootScope.exerciseDetails.stack.variant;
			if($scope.tmpNewExercise.variant==undefined || $scope.tmpNewExercise.variant == "")
				$scope.tmpNewExercise.variant = "Default";

			document.querySelector('#solutionMDEditor').innerHTML = "";
			var sol = "";
			if(undefined != $scope.exerciseDetails.solution && undefined != $scope.exerciseDetails.solution.text){
				sol = $scope.exerciseDetails.solution.text;
				$scope.tmpNewExercise.solution = $scope.exerciseDetails.solution;
			}
			else{
				$scope.tmpNewExercise.solution = { text : ""};
			}

			for(var i=0; i<$rootScope.stackItems.length;i++){
				if($rootScope.stackItems[i].technology == $rootScope.exerciseDetails.stack.technology && $rootScope.stackItems[i].vulnerability == $rootScope.exerciseDetails.stack.vulnerability){
					server.loadStackKB($rootScope.stackItems[i].uuid);
					break;
				}
			}
			

			var solutionMDEditor = new toastui.Editor({
				el: document.querySelector('#solutionMDEditor'),
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				height: '405px',
				initialEditType: 'markdown',
				hideModeSwitch: true,
				usageStatistics:false,
				initialValue: '',
				events: {
					change: function() {
						$scope.tmpNewExercise.solution.text = solutionMDEditor.getMarkdown();
					}
				}
			});

			var info = "";
			if(undefined != $scope.tmpNewExercise.information && undefined != $scope.tmpNewExercise.information.text)
				info = $scope.tmpNewExercise.information.text;
			else
				$scope.tmpNewExercise.information = { text : ""};

			document.querySelector('#EDInfoMDEditor').innerHTML = "";
			var infoMDEditor = new toastui.Editor({
				el: document.querySelector('#EDInfoMDEditor'),
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				height: '300px',
				usageStatistics:false,
				initialEditType: 'markdown',
				hideModeSwitch: true,
				initialValue: '',
				events: {
					change: function() {
						$scope.tmpNewExercise.information.text = infoMDEditor.getMarkdown();
					},
				}
			});

			$scope.tmpNewExercise.flags = $rootScope.exerciseDetails.flags;
			$scope.newExerciseFlagList = true;
			$('#addNewExerciseModal').modal('show');
			solutionMDEditor.setMarkdown(sol);
			infoMDEditor.setMarkdown(info);

		}catch(e){
			PNotify.removeAll();
			notificationService.notice('An error occured, please try again.');
		}
	}

	$scope.$on('exerciseUpdated:updated', function(event,data) {

		$rootScope.showExerciseDetails = false;
		$rootScope.showExerciseList = true;
		$location.path("available-exercises", false);

		server.getAvailableExercises();

		initEmptyExercise();

		$scope.newExerciseFlagList = true;
		$scope.saveFlow = false;

		$('#addNewExerciseModal').modal('hide');

	});

	$scope.clearExerciseModal = function(){

		initEmptyExercise();
		$scope.newExerciseFlagList = true;
		$scope.saveFlow = false;
	}


	$scope.$on('exerciseAdded:updated', function(event,data) {

		$scope.newExerciseFlagList = true;
		$scope.saveFlow = false;
		initEmptyExercise();
		$('#addNewExerciseModal').modal('hide');
		server.getAvailableExercises();
		if(undefined!=$scope.tmpExerciseImage && undefined!=$scope.tmpExerciseImage.imageUrl){
			$scope.tmpExerciseImage.idExercise = data.id;
			$('#importTaskDefinitionModal').modal('show');
		}

	});

	$scope.importTaskDefinition = function(){

		for(var i=0;i<$scope.tmpExerciseImage.deployTo.length;i++){

			$scope.newTaskDefinition.exerciseId = $scope.tmpExerciseImage.idExercise
			$scope.newTaskDefinition.region = $scope.tmpExerciseImage.deployTo[i];
			$scope.newTaskDefinition.softMemory = $scope.tmpExerciseImage.softMemory;
			$scope.newTaskDefinition.hardMemory = $scope.tmpExerciseImage.hardMemory;
			$scope.newTaskDefinition.status = true;
			$scope.newTaskDefinition.imageUrl = $scope.tmpExerciseImage.imageUrl;
			$scope.newTaskDefinition.containerName = $scope.tmpExerciseImage.containerName;
			$scope.newTaskDefinition.taskDefinitionName = $scope.tmpExerciseImage.taskDefinitionName;
			if($scope.tmpExerciseImage.taskDefinitionName.indexOf(':')>-1)
				$scope.newTaskDefinition.taskDefinitionName = $scope.tmpExerciseImage.taskDefinitionName.substr(0,$scope.tmpExerciseImage.taskDefinitionName.indexOf(':'));
			let obj1 = cloneObj($scope.newTaskDefinition)
			server.addTaskDefinition(obj1);

		}
		$('#importTaskDefinitionModal').modal('hide');
	}

	$scope.tmpExerciseImage.deployTo = [];
	$scope.toggleDeployToSelection = function(reg) {
		var idx = $scope.tmpExerciseImage.deployTo.indexOf(reg);
		if (idx > -1) {
			$scope.tmpExerciseImage.deployTo.splice(idx, 1);
		}
		else {
			$scope.tmpExerciseImage.deployTo.push(reg);
		}
	};

	$scope.removeNewFlag = function(t,c){
		for(var i=0; i<$scope.tmpNewExercise.flags.length; i++){
			if($scope.tmpNewExercise.flags[i].title == t && $scope.tmpNewExercise.flags[i].category == c){
				$scope.tmpNewExercise.flags.remove(i,i);
				return;
			}
		}
	}

	$scope.addNewFlag = function(){

		if($scope.tmpFlag.hintAvailable){
			if($scope.tmpFlag.hint.scoreReducePercentage==null){
				PNotify.removeAll();
				notificationService.notice('Please provide score reduction for hint');
				return;
			}
			try{
				hintReduction = parseInt($scope.tmpFlag.hint.scoreReducePercentage);
			}catch(e){
				PNotify.removeAll();
				notificationService.notice('Please provide score reduction for hint');
				return;
			}
		}
		if($scope.tmpFlag.hintAvailable && $scope.tmpFlag.hint.md.text==""){
			PNotify.removeAll();
			notificationService.notice('Please provide text for hint');
			return;
		}
		if($scope.tmpFlag.md.text == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide text for instructions');
			return;
		}
		if($scope.tmpFlag.selfCheckAvailable && $scope.tmpFlag.selfCheck.name==""){
			PNotify.removeAll();
			notificationService.notice('Please provide self-check identifier');
			return;
		}
		if($scope.tmpFlag.selfCheckAvailable && $scope.tmpSelfCheckMappings.length<2){
			PNotify.removeAll();
			notificationService.notice('Please define at least one status mapping to "Vulnerable" and one to "Not Vulnerable"');
			return;
		}

		var obj2 = {};
		var obj = {};

		obj.title = $scope.tmpFlag.title;
		obj.kb = $scope.tmpFlag.KBItem;
		obj.category = $scope.tmpFlag.KBItem.category;
		obj.flagList = [];

		obj2.selfCheck = $scope.tmpFlag.selfCheck;
		if(undefined==obj2.selfCheck)
			obj2.selfCheck = {};
		obj2.selfCheck.messageMappings = {};
		obj2.selfCheck.statusMapping = {};

		for(var i=0;i<$scope.tmpSelfCheckMappings.length;i++){
			obj2.selfCheck.messageMappings[$scope.tmpSelfCheckMappings[i].status] = $scope.tmpSelfCheckMappings[i].message;
			obj2.selfCheck.statusMapping[$scope.tmpSelfCheckMappings[i].status] = $scope.tmpSelfCheckMappings[i].mapping;
		}
		obj2.selfCheckAvailable = $scope.tmpFlag.selfCheckAvailable;
		obj2.type = $scope.tmpFlag.type;
		obj2.hint = $scope.tmpFlag.hint;
		obj2.hint.type = obj2.type;
		obj2.hintAvailable = $scope.tmpFlag.hintAvailable;
		obj2.md = {};
		obj2.md.text = $scope.tmpFlag.md.text;
		obj2.optional = $scope.tmpFlag.optional;
		if(obj2.optional)
			obj2.maxScore = 0;
		else
			obj2.maxScore = $scope.tmpFlag.maxScore;

		obj.flagList.push(obj2);
		$scope.tmpNewExercise.flags.push(obj);

		$scope.newExerciseFlagList = true;

		$scope.tmpFlag = {};
		$scope.tmpFlag.title = "";
		$scope.tmpFlag.selfCheck = { name: "", messageMappings: {}, statusMapping: {}};
		$scope.tmpFlag.selfCheckAvailable = false;
		$scope.tmpFlag.hint = { md: { text : ""}, type: "", scoreReducePercentage: ""};
		$scope.tmpFlag.hintAvailable  = false;
		$scope.tmpFlag.maxScore = "";
		$scope.tmpFlag.optional = "";
		$scope.tmpFlag.type = "";
		$scope.tmpFlag.md = {};
		$scope.tmpFlag.md.text = "";
		$scope.tmpFlag.KBItem = "";
		$scope.tmpCheckerStatus = "";
		$scope.tmpCheckerMapping = "";
		$scope.tmpCheckerMessage = "";
		$scope.tmpSelfCheckMappings = [];

	}

	getObjectFromStatus = function(status){
		for(var i in $rootScope.vulnerabilityStatus){
			if ($rootScope.vulnerabilityStatus[i].id == status){
				return $rootScope.vulnerabilityStatus[i];
			}
		}
	}
	$scope.updateNewFlag = function(){

		if($scope.tmpFlag.hintAvailable){
			if($scope.tmpFlag.hint.scoreReducePercentage==null){
				PNotify.removeAll();
				notificationService.notice('Please provide score reduction for hint');
				return;
			}
			try{
				hintReduction = parseInt($scope.tmpFlag.hint.scoreReducePercentage);
			}catch(e){
				PNotify.removeAll();
				notificationService.notice('Please provide score reduction for hint');
				return;
			}
		}
		if($scope.tmpFlag.hintAvailable && $scope.tmpFlag.hint==""){
			PNotify.removeAll();
			notificationService.notice('Please provide text for hint');
			return;
		}
		if($scope.tmpFlag.md.text == ""){
			PNotify.removeAll();
			notificationService.notice('Please provide text for instructions');
			return;
		}
		if($scope.tmpFlag.selfCheckAvailable && $scope.tmpFlag.selfCheck.name==""){
			PNotify.removeAll();
			notificationService.notice('Please provide self-check identifier');
			return;
		}
		if($scope.tmpFlag.selfCheckAvailable && $scope.tmpSelfCheckMappings.length<2){
			PNotify.removeAll();
			notificationService.notice('Please define at least one status mapping to "Vulnerable" and one to "Not Vulnerable"');
			return;
		}

		var obj2 = {};
		var obj = {};

		obj.title = $scope.tmpFlag.title;
		obj.kb = $scope.tmpFlag.KBItem;
		obj.id = $scope.tmpFlag.id;
		obj.category = $scope.tmpFlag.KBItem.category
		obj.flagList = [];

		obj2.selfCheckAvailable = $scope.tmpFlag.selfCheckAvailable;

		if(obj2.selfCheckAvailable){
			obj2.selfCheck = $scope.tmpFlag.selfCheck;
			obj2.selfCheck.messageMappings = {}
			obj2.selfCheck.statusMapping = {}

			for(var i=0;i<$scope.tmpSelfCheckMappings.length;i++){
				obj2.selfCheck.messageMappings[$scope.tmpSelfCheckMappings[i].status] = $scope.tmpSelfCheckMappings[i].message;
				obj2.selfCheck.statusMapping[$scope.tmpSelfCheckMappings[i].status] = $scope.tmpSelfCheckMappings[i].mapping.id;
			}
		}
		obj2.type = $scope.tmpFlag.type;

		obj2.hintAvailable = $scope.tmpFlag.hintAvailable;
		if(obj2.hintAvailable){
			obj2.hint = $scope.tmpFlag.hint;
			obj2.hint.type = obj2.type;
		}
		obj2.md = {};
		obj2.md.text = $scope.tmpFlag.md.text;
		obj2.optional = $scope.tmpFlag.optional;
		if(obj2.optional)
			obj2.maxScore = 0;
		else
			obj2.maxScore = $scope.tmpFlag.maxScore;

		obj.flagList.push(obj2);

		for(var j in $scope.tmpNewExercise.flags){
			if($scope.tmpNewExercise.flags[j].id == $scope.tmpFlag.id){
				$scope.tmpNewExercise.flags[j] = obj;
			}
		}

		$scope.newExerciseFlagList = true;

		$scope.tmpFlag = {};
		$scope.tmpFlag.title = "";
		$scope.tmpFlag.selfCheck = { name: "", messageMappings: {}, statusMapping: {}};
		$scope.tmpFlag.selfCheckAvailable = false;
		$scope.tmpFlag.hint = { md: { text : ""}, type: "", scoreReducePercentage: ""};
		$scope.tmpFlag.hintAvailable  = false;
		$scope.tmpFlag.maxScore = "";
		$scope.tmpFlag.optional = "";
		$scope.tmpFlag.type = "";
		$scope.tmpFlag.md = {};
		$scope.tmpFlag.md.text = "";
		$scope.tmpFlag.KBItem = "";
		$scope.tmpCheckerStatus = "";
		$scope.tmpCheckerMapping = "";
		$scope.tmpCheckerMessage = "";
		$scope.tmpSelfCheckMappings = [];
	}
	$scope.flagSaveFlow = false;
	$scope.editNewFlagDialog = function(flag){
		if($scope.newExerciseFlagList){
			$scope.newExerciseFlagList = false;
			$scope.flagSaveFlow = true;
			$scope.tmpFlag = {};
			$scope.tmpFlag.id = flag.id
			$scope.tmpFlag.title = flag.title;
			$scope.tmpFlag.selfCheck = flag.flagList[0].selfCheck
			$scope.tmpFlag.selfCheckAvailable = flag.flagList[0].selfCheckAvailable
			$scope.tmpFlag.hint = flag.flagList[0].hint;
			$scope.tmpFlag.hintAvailable  = flag.flagList[0].hintAvailable;
			$scope.tmpFlag.maxScore = flag.flagList[0].maxScore;
			$scope.tmpFlag.optional = flag.flagList[0].optional;
			$scope.tmpFlag.type = flag.flagList[0].type;
			$scope.tmpFlag.md = {};
			$scope.tmpFlag.md.text = flag.flagList[0].md.text;
			$scope.tmpFlag.KBItem = flag.kb;
			$scope.tmpCheckerStatus = "";
			$scope.tmpCheckerMapping = "";
			$scope.tmpCheckerMessage = "";
			$scope.tmpSelfCheckMappings = [];
			if($scope.tmpFlag.selfCheckAvailable){
				for(var i in $scope.tmpFlag.selfCheck.statusMapping){
					if ($scope.tmpFlag.selfCheck.statusMapping.hasOwnProperty(i)){
						var obj = {};
						obj.status = i;
						obj.mapping = getObjectFromStatus($scope.tmpFlag.selfCheck.statusMapping[i]);
						obj.message = $scope.tmpFlag.selfCheck.messageMappings[i];
						$scope.tmpSelfCheckMappings.push(obj);
					}
				}

			}

			document.querySelector('#tmpFlagInstructions').innerHTML = "";
			var instructionsEditor = new toastui.Editor({
				el: document.querySelector('#tmpFlagInstructions'),
				height: '220px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				initialValue: '',
				initialEditType: 'markdown',
				hideModeSwitch: true,
				usageStatistics:false,
				events: {
					change: function() {
						$scope.tmpFlag.md.text = instructionsEditor.getMarkdown();
					},
				}
			}); 
			document.querySelector('#tmpFlagHint').innerHTML = "";
			if($scope.tmpFlag.hint == undefined || $scope.tmpFlag.hint.md == undefined || $scope.tmpFlag.hint.md.text == undefined){
				$scope.tmpFlag.hint = {};
				$scope.tmpFlag.hint.md = {}
				$scope.tmpFlag.hint.md.text = "";
			}
			var hintEditor = new toastui.Editor({
				el: document.querySelector('#tmpFlagHint'),
				height: '150px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				usageStatistics:false,
				initialEditType: 'markdown',
				hideModeSwitch: true,
				viewer:true,
				initialValue: '',
				events: {
					change: function() {
						$scope.tmpFlag.hint.md.text = hintEditor.getMarkdown();
					},
				}
			}); 

			document.querySelector('#tmpCheckerMessage').innerHTML = "";
			checkerMessageEditor = new toastui.Editor({
				el: document.querySelector('#tmpCheckerMessage'),
				height: '150px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				usageStatistics:false,
				initialValue: "",
				events: {
					change: function() {
						$scope.tmpCheckerMessage = checkerMessageEditor.getMarkdown();
					},
				}
			}); 
			if($scope.tmpFlag.hintAvailable)
				hintEditor.setMarkdown($scope.tmpFlag.hint.md.text)
				instructionsEditor.setMarkdown($scope.tmpFlag.md.text);
		}
		else{
			$scope.newExerciseFlagList = true;
		}
	}

	$scope.addNewFlagDialog = function(){
		if($scope.newExerciseFlagList){
			$scope.newExerciseFlagList = false;
			$scope.flagSaveFlow = false;
			document.querySelector('#tmpFlagInstructions').innerHTML = "";
			$scope.tmpFlag.md = {};
			$scope.tmpFlag.md.text = "";
			$scope.tmpFlag.hint = {};
			$scope.tmpFlag.hint.md = {};
			$scope.tmpFlag.hint.md.text = "";
			var instructionsEditor = new toastui.Editor({
				el: document.querySelector('#tmpFlagInstructions'),
				height: '220px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				initialValue: "",
				initialEditType: 'markdown',
				hideModeSwitch: true,
				usageStatistics:false,
				events: {
					change: function() {
						$scope.tmpFlag.md.text = instructionsEditor.getMarkdown();
					},
				}
			}); 
			document.querySelector('#tmpFlagHint').innerHTML = "";
			var hintEditor = new toastui.Editor({
				el: document.querySelector('#tmpFlagHint'),
				height: '150px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				usageStatistics:false,
				initialValue: "",
				initialEditType: 'markdown',
				hideModeSwitch: true,
				events: {
					change: function() {
						$scope.tmpFlag.hint.md.text = hintEditor.getMarkdown();
					},
				}
			}); 
			document.querySelector('#tmpCheckerMessage').innerHTML = "";
			checkerMessageEditor = new toastui.Editor({
				el: document.querySelector('#tmpCheckerMessage'),
				height: '150px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				usageStatistics:false,
				initialValue: "",
				initialEditType: 'markdown',
				hideModeSwitch: true,
				events: {
					change: function() {
						$scope.tmpCheckerMessage = checkerMessageEditor.getMarkdown();
					},
				}
			}); 
		}
		else{
			$scope.newExerciseFlagList = true;
		}
	}


	$scope.getColorForScore = function(score){
		if(score<=20)
			return "rgba(118, 147, 193, 0.94)";
		if(score<=50)
			return "rgba(158, 74, 114, 0.87)";
		if(score<=75)
			return "rgba(118, 118, 193, 0.94)";
		if(score<=100)
			return "rgba(106, 106, 125, 0.87)";
		if(score<=125)
			return "rgba(56, 31, 8, 0.87)";
		return "rgba(189, 108, 34, 0.87)";
	}


	$scope.getExerciseDetails = function(uuid){
		server.getExerciseDetails(uuid);
	}



	function isKbPresent(kb){
		if(undefined==kb)
			return false;
		for(var j=0; j<$scope.exerciseKbs.length; j++){
			if($scope.exerciseKbs[j].uuid==kb.uuid)
				return true;
		}
		return false;
	}
	$scope.$on('vulnKBLoaded:updated', function(event,data) {

		if($rootScope.visibility.availableExercises){
			var cMd = data.md.text+"\n";
			if(data.kbMapping!=undefined){
				for(var i=0;i<Object.keys(data.kbMapping).length;i++){
					var tmpInner = data.kbMapping[Object.keys(data.kbMapping)[i]]
					cMd += "\n***\n# "+tmpInner.technology+" #\n"+tmpInner.md.text+"\n";
				}
			}
			document.querySelector('#kbMD').innerHTML = '';
			var editor = new toastui.Editor.factory({
				el: document.querySelector('#kbMD'),
				viewer: true,
				usageStatistics:false,
				height: '500px',
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				initialValue: ''
			});
			editor.setMarkdown(cMd);
			$('#kbModal').modal('show');
			autoplayMdVideo('#kbMD');
			var kbFound = false;
			for(var j=0; j<$rootScope.kbItems.length; j++){
				if($rootScope.kbItems[j].uuid == data.uuid){
					$rootScope.kbItems[j] = data;
					kbFound = true;
					break;
				}
			}
			if(!kbFound){
				$rootScope.kbItems.push(data)
			}
		}
	})

	$scope.openVulnKB = function(item,technology){

		for(var j=0; j<$rootScope.kbItems.length; j++){
			if($rootScope.kbItems[j].technology == item.technology && $rootScope.kbItems[j].vulnerability  == item.vulnerability){
				server.loadVulnKBTechnology($rootScope.kbItems[j].uuid,technology);
				return;
			}
		}
	}

	$rootScope.exerciseDetails = [];
	$scope.$on('exerciseDetails:updated', function(event,data) {

		$rootScope.exerciseDetails = data;
		$scope.exerciseKbs = []; 
		var stackFound = false;
		if(undefined!=$rootScope.exerciseDetails.stack && undefined!=$rootScope.exerciseDetails.stack.md && undefined!=$rootScope.exerciseDetails.stack.md.text){
			for(var k=0; k<$rootScope.stackItems.length; k++){
				if($rootScope.stackItems[k].uuid == $rootScope.exerciseDetails.stack.uuid){
					$rootScope.stackItems[k] = $rootScope.exerciseDetails.stack;
					stackFound = true;
					break;
				}
			}
			if(!stackFound){
				$rootScope.stackItems.push($rootScope.exerciseDetails.stack)
			}
		}
		else{
			for(var i=0; i<$rootScope.stackItems.length;i++){
				if($rootScope.stackItems[i].technology == $rootScope.exerciseDetails.stack.technology && $rootScope.stackItems[i].variant == $rootScope.exerciseDetails.stack.variant){
					server.loadStackKB($rootScope.stackItems[i].uuid);
					break;
				}
			}
		}
		var kbFound = false;
		for(var i=0; i<$rootScope.exerciseDetails.flags.length; i++){
			if(undefined!=$rootScope.exerciseDetails.flags[i].kb){
				if(!isKbPresent($rootScope.exerciseDetails.flags[i].kb))
					$scope.exerciseKbs.push($rootScope.exerciseDetails.flags[i].kb);
			}
			if(undefined != $rootScope.exerciseDetails.flags[i].kb.md && undefined != $rootScope.exerciseDetails.flags[i].kb.md.text){
				for(var j=0; j<$rootScope.kbItems.length; j++){
					if($rootScope.kbItems[j].uuid == $rootScope.exerciseDetails.flags[i].kb.uuid){
						$rootScope.kbItems[j] = $rootScope.exerciseDetails.flags[i].kb;
						kbFound = true;
						break;
					}
				}
				if(!kbFound){
					$rootScope.kbItems.push($rootScope.exerciseDetails.flags[i].kb)
				}
			}
		}	
		if($rootScope.exerciseDetails.information != undefined){
			document.querySelector("#exerciseInfoMD").innerHTML = "";
			var editor = new toastui.Editor.factory({
				viewer: true,
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				usageStatistics:false,
				el: document.querySelector("#exerciseInfoMD"),
				initialValue: $rootScope.exerciseDetails.information.text
			});
		}
		autoplayMdVideo('#exerciseInfoMD');
		if(undefined!=$rootScope.exerciseDetails.stack.uuid)
			server.loadStackKB($rootScope.exerciseDetails.stack.uuid);
		if($rootScope.exerciseDetails.solution != undefined){
			document.querySelector("#solutionMDViewer").innerHTML = "";
			var editor = new toastui.Editor.factory({
				viewer: true,
				plugins: [ codeSyntaxHightlight, table, colorSyntax ],
				usageStatistics:false,
				el: document.querySelector("#solutionMDViewer"),
				initialValue: $rootScope.exerciseDetails.solution.text
			});
		}
		autoplayMdVideo('#solutionMDViewer');
		$rootScope.showExerciseDetails = true;
		$rootScope.showExerciseList = false;


		$scope.triggerFlagsMarkdown = function(fq,index){
			window.setTimeout(function(){
				try{
					if(undefined != fq){
						document.querySelector('#fe'+index+'-md').innerHTML = '';
						var editor = new toastui.Editor.factory({
							el: document.querySelector('#fe'+index+'-md'),
							viewer: true,
							usageStatistics:false,
							plugins: [ codeSyntaxHightlight, table, colorSyntax ],
							height: '500px',
							initialValue: fq.md.text
						});
						autoplayMdVideo('#fe'+index+'-md');
						$('#fe'+index+'-md').find('a').each(function() {
							if(this.href==undefined || this.href=="")
								return;
							if(this.href.indexOf("#exerciseKB")>=0){
								$(this).replaceWith($(this).text());
							}
						});
					}
				}catch(e){}
			},100);
		}

		$location.path("available-exercises/details/"+$rootScope.exerciseDetails.uuid, false);
	});


	var tmpExerciseToRemove = -1;
	$scope.removeExerciseModal = function(id,name){
		tmpExerciseToRemove = id;
		$scope.tmpExerciseToBeRemovedName = name
		$('#removeExerciseModal').modal('show');
	}
	$scope.removeExercise = function(){
		server.removeExercise(tmpExerciseToRemove);
		tmpExerciseToRemove = -1;
		$('#removeExerciseModal').modal('hide');
	}

	$scope.backToList = function(){
		$rootScope.showExerciseList = true;
		$rootScope.showExerciseDetails = false;
	}


	$scope.getExerciseStatusString = function(status){
		switch(status){
		case "0":
			return "Available";
			break;
		case "2":
			return "Coming Soon";
			break;
		case "3":
			return "Inactive";
			break;
		default:
			return "N/A";
		}
	}


	$scope.updateAvailableExercisesFilteredList = function() {
		$scope.filteredAvailableExercisesList = $filter("filter")($scope.masterAvailableExercisesList, $scope.queryAvailableExercises);
	};
	$scope.availableExercisestableconfig = {
			itemsPerPage: 20,
			fillLastPage: false
	}
	$scope.$on('availableExercises:updated', function(event,data) {
		$scope.masterAvailableExercisesList = data;
		$scope.filteredAvailableExercisesList = cloneObj($scope.masterAvailableExercisesList);
	});



}]);