!function(n){function e(i){if(t[i])return t[i].exports;var r=t[i]={i:i,l:!1,exports:{}};return n[i].call(r.exports,r,r.exports,e),r.l=!0,r.exports}var t={};e.m=n,e.c=t,e.d=function(n,t,i){e.o(n,t)||Object.defineProperty(n,t,{configurable:!1,enumerable:!0,get:i})},e.n=function(n){var t=n&&n.__esModule?function(){return n.default}:function(){return n};return e.d(t,"a",t),t},e.o=function(n,e){return Object.prototype.hasOwnProperty.call(n,e)},e.p="",e(e.s=0)}([function(n,e,t){function i(){return self.registration.pushManager.getSubscription().then(function(n){if(null===n)return o()})}function r(){return self.registration.pushManager.getSubscription().then(function(n){return c(n,b.Unsubscribe),null!==n&&n.unsubscribe()})}function o(){a().then(function(n){var e=p(n.public_key),t={applicationServerKey:e,userVisibleOnly:!0};return self.registration.pushManager.subscribe(t).then(function(n){return c(n,b.Subscribe)})})}function a(){return l().then(function(){var n={FAID:d().FAID,bundleId:d().bundleId,deviceId:d().deviceId,sdkPlatform:"Web"};return s(f("webpush_key"),n)})}function c(n,e){var t=u(n,e);return s(f("notification"),t)}function u(n,e){var t=n?n.endpoint:null,i=n?n.getKey("p256dh"):null,r=n?n.getKey("auth"):null,o=i?btoa(String.fromCharCode.apply(null,new Uint8Array(i))):null,a=r?btoa(String.fromCharCode.apply(null,new Uint8Array(r))):null;return{FAID:d().FAID,deviceId:d().deviceId,bundleId:d().bundleId,deviceToken:t,acceptBadge:Boolean(e),acceptSound:Boolean(e),acceptAlert:Boolean(e),sdkPlatform:"Web",publicKey:o,auth:a}}function s(n,e){return fetch(n,{method:"post",headers:{"Content-type":"application/json"},body:JSON.stringify(e)}).then(function(n){return 200!==n.status?void console.log("Fetch Service Error. Status Code: "+n.status):n.json().then(function(n){if(n.success)return n.result;console.log("Fetch Service Failure :: "+n.errorMessage)})}).catch(function(n){console.log("Fetch Service Resolve Error :: ",n)})}function l(){var n={FAID:d().FAID,sdkPlatform:"Web",sdkVersion:h};return s(f("deployment"),n).then(function(n){return v=n.service_domain})}function f(n){var e="deployment"===n?"auth":v;return d().envProtocol+"://"+e+(""===d().env?".":d().env+".")+d().envDomain+"/api/"+n}function d(){var n=self.location.search.substr(1),e=n.split("&"),t={};return e.forEach(function(n){var e=n.split("="),i=decodeURIComponent(e[0]),r=decodeURIComponent(e[1]);t[i]=r}),t}function p(n){for(var e="=".repeat((4-n.length%4)%4),t=(n+e).replace(/\-/g,"+").replace(/_/g,"/"),i=atob(t),r=new Uint8Array(i.length),o=0;o<i.length;++o)r[o]=i.charCodeAt(o);return r}var b,h="1.1.0";!function(n){n[n.Unsubscribe=0]="Unsubscribe",n[n.Subscribe=1]="Subscribe"}(b||(b={}));var v="";self.addEventListener("install",function(n){return n.waitUntil(self.skipWaiting())}),self.addEventListener("activate",function(n){return n.waitUntil(self.clients.claim())}),self.addEventListener("message",function(n){switch(n.data){case"registerForPushNotification":i();break;case"unregisterFromPushNotification":r()}}),self.addEventListener("push",function(n){if(self.Notification&&"granted"===self.Notification.permission){var e={};n.data&&(e=JSON.parse(n.data.text()));var t=e,i=t.title,r=t.body,o=t.image,a=t.action,c=t.data;if(c.hasOwnProperty("FA")&&c.FA.hasOwnProperty("id")){var u={action:a,id:c.FA.id},s=o&&o.trim().length>0?o:d().defaultIcon,l={action:a,body:r,icon:"null"===s?null:s,data:u},f=self.registration.showNotification(i,l);n.waitUntil(f)}}}),self.addEventListener("notificationclick",function(n){var e=(self.location.origin||self.location.origin,n.notification.data),t=e.id,i=e.action;i=null===i?"":i;var r,o=i.includes("?")?"&":"?",a=""+i+o+"fa_cid="+t;try{r=new URL(a,self.location.origin).href}catch(n){r=new URL("fa_cid="+t,self.location.origin).href}n.notification.close();var c=self.clients.openWindow(r);n.waitUntil(c)}),self.addEventListener("pushsubscriptionchange",function(n){n.waitUntil(a().then(function(n){var e=p(n.public_key),t={applicationServerKey:e,userVisibleOnly:!0};return self.registration.pushManager.subscribe(t).then(function(n){return c(n,b.Subscribe)})}))})}]);