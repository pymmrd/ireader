/*!
 * jQuery Cookie Plugin v1.3.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD. Register as anonymous module.
		define(['jquery'], factory);
	} else {
		// Browser globals.
		factory(jQuery);
	}
}(function ($) {

	var pluses = /\+/g;

	function decode(s) {
		if (config.raw) {
			return s;
		}
		try {
			// If we can't decode the cookie, ignore it, it's unusable.
			return decodeURIComponent(s.replace(pluses, ' '));
		} catch(e) {}
	}

	function decodeAndParse(s) {
		if (s.indexOf('"') === 0) {
			// This is a quoted cookie as according to RFC2068, unescape...
			s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
		}

		s = decode(s);

		try {
			// If we can't parse the cookie, ignore it, it's unusable.
			return config.json ? JSON.parse(s) : s;
		} catch(e) {}
	}

	var config = $.cookie = function (key, value, options) {

		// Write
		if (value !== undefined) {
			options = $.extend({}, config.defaults, options);

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setDate(t.getDate() + days);
			}

			value = config.json ? JSON.stringify(value) : String(value);

			return (document.cookie = [
				config.raw ? key : encodeURIComponent(key),
				'=',
				config.raw ? value : encodeURIComponent(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// Read

		var result = key ? undefined : {};

		// To prevent the for loop in the first place assign an empty array
		// in case there are no cookies at all. Also prevents odd result when
		// calling $.cookie().
		var cookies = document.cookie ? document.cookie.split('; ') : [];

		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			var name = decode(parts.shift());
			var cookie = parts.join('=');

			if (key && key === name) {
				result = decodeAndParse(cookie);
				break;
			}

			// Prevent storing a cookie that we couldn't decode.
			if (!key && (cookie = decodeAndParse(cookie)) !== undefined) {
				result[name] = cookie;
			}
		}

		return result;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) !== undefined) {
			// Must not alter options, thus extending a fresh object...
			$.cookie(key, '', $.extend({}, options, { expires: -1 }));
			return true;
		}
		return false;
	};

}));

$(function(){
	var speed = 5;
	var autopage;// = $.cookie("autopage");
	var night;
	var timer;
	var temPos=1;
	function scrolling() 
	{  
		var currentpos=1;
		if($.browser.is=="chrome" |document.compatMode=="BackCompat" ){
			currentpos=document.body.scrollTop;
		}else{
			currentpos=document.documentElement.scrollTop;
		}

		window.scroll(0,++currentpos);
		if($.browser.is=="chrome" || document.compatMode=="BackCompat" ){
			temPos=document.body.scrollTop;
		}else{
			temPos=document.documentElement.scrollTop;
		}

		if(currentpos!=temPos){
			///msie/.test( userAgent )
			var autopage = $.cookie("autopage");
			if(autopage==1&&/next_page/.test( document.referrer ) == false) location.href=next_page;
			sc();
		}
	}

	function scrollwindow(){
		timer=setInterval("scrolling()",250/speed);
	}

	function sc(){ 
		clearInterval(timer); 
	}

	function setSpeed(ispeed){ 
		if(ispeed==0)ispeed=5;
		speed=ispeed;
		$.cookie("scrollspeed",ispeed,{path:'/',expires:365});
	}

	function setAutopage(){
		if($('#autopage').is(":checked") == true){
			$('#autopage').attr("checked",true);	
			$.cookie("autopage",1,{path:'/',expires:365});
		}else{
			$('#autopage').attr("checked",false);
			$.cookie("autopage",0,{path:'/',expires:365});
		}
	}
	autopage = $.cookie("autopage");
	sbgcolor = $.cookie("bcolor");
	setBGColor(sbgcolor);
	font = $.cookie("font");
	setFont(font);
	size = $.cookie("size");
	setSize(size);
	color = $.cookie("color");
	setColor(color);
	width = $.cookie("width");
	setWidth(width);
	speed = $.cookie("scrollspeed");
	if(autopage==1) {
		$('#autopage').attr("checked",true);
		speed = $.cookie("scrollspeed");
		scrollwindow();
	}
	night = $.cookie('night');
	if(night==1) {
		$("#night").attr('checked',true);
		setNight();
	}
	document.onmousedown=sc;
	document.ondblclick=scrollwindow;

if (typeof(getCookie("bgcolor")) != 'undefined') {
    wrapper.style.background = getCookie("bgcolor");
    document.getElementById("bcolor").value = getCookie("bgcolor")
}

function changebgcolor(id) {
    wrapper.style.background = id.options[id.selectedIndex].value;
    setCookie("bgcolor", id.options[id.selectedIndex].value, 365)
}
function setBGColor(sbgcolor){
	$('#wrapper').css("backgroundColor",sbgcolor);
	$.cookie("bcolor",sbgcolor,{path:'/',expires:365});
}
function setColor(color) {
	$("#content").css("color",color);
	$.cookie("color",color,{path:'/',expires:365});
}
function setSize(size) {
	$("#content").css("fontSize",size);
	$.cookie("size",size,{path:'/',expires:365});
}
function setFont(font) {
	$("#content").css("fontFamily",font);
	$.cookie("font",font,{path:'/',expires:365});
}
function setWidth(width){
	$('#content').css("width",width);
	$.cookie("width",width,{path:'/',expires:365});
}
function setNight(){
	if($("#night").attr('checked')==true) {
		$('div').css("backgroundColor","#111111");
		$('div,a').css("color","#939392");
		$.cookie("night",1,{path:'/',expires:365});
	} else {
		$('div').css("backgroundColor","");
		$('div,a').css("color","");
		$.cookie("night",0,{path:'/',expires:365});
	}
}

function setCookie(name, value, day) {
    var exp = new Date();
    exp.setTime(exp.getTime() + day * 24 * 60 * 60 * 1000);
    document.cookie = name + "= " + escape(value) + ";expires= " + exp.toGMTString()
}
function getCookie(objName) {
    var arrStr = document.cookie.split("; ");
    for (var i = 0; i < arrStr.length; i++) {
        var temp = arrStr[i].split("=");
        if (temp[0] == objName) return unescape(temp[1])
    }
}
});
