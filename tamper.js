// ==UserScript==
// @name         Twitch clip downloader
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Brian Lee
// @match        https://*clips.twitch.tv/*
// @run-at       document-idle
// @require      https://code.jquery.com/jquery-3.1.1.min.js
// ==/UserScript==

(function() {
    'use strict';

    // might find a better way to automate clip downloading.
    // see if can figure out a way to dl the entire 1min clip instead of 30s

    // look into PhantomJS
    // http://phantomjs.org/download.html

    let editClipBtn = document.getElementsByClassName('button align-center full-width ce-button-fancy')[0];
    editClipBtn.click();

    let publishBtn = document.querySelector("a.button.full-width.button--large.align-center");
    publishBtn.click();

})();
