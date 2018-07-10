/* Copyright 2017 Google LLC
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*    http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
(function(exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", {
        value: true
    });
    function runPhase(rules, inString) {
        var outString = "";
        var midString = inString;
        var startOfString = true;
        while (midString.length > 0) {
            var foundRule = false;
            for (var _i = 0, rules_1 = rules; _i < rules_1.length; _i++) {
                var rule = rules_1[_i];
                if (rule.matchOnStart == null || startOfString) {
                    var m = midString.match(rule.p);
                    if (m != null) {
                        foundRule = true;
                        var rightPartSize = midString.length - m[0].length;
                        midString = midString.replace(rule.p, rule.s);
                        var newStart = midString.length - rightPartSize;
                        if (rule.revisit == null) {
                            outString += midString.substring(0, newStart);
                            midString = midString.substring(newStart);
                        }
                    }
                }
            }
            if (!foundRule) {
                outString += midString[0];
                midString = midString.substring(1);
            }
            startOfString = false;
        }
        return outString;
    }
    function runAllPhases(allRules, inString) {
        var outString = inString;
        for (var _i = 0, allRules_1 = allRules; _i < allRules_1.length; _i++) {
            var rules = allRules_1[_i];
            outString = runPhase(rules, outString);
        }
        return outString;
    }
    function getAllRulesZ2U() {
        var rules0 = [ {
            p: RegExp("^" + "([က-အ])်ၤ"),
            s: "င်္$1ျ"
        }, {
            p: RegExp("^" + "([က-အ])ၤ"),
            s: "င်္$1"
        }, {
            p: RegExp("^" + "ၤ"),
            s: "င်္"
        }, {
            p: RegExp("^" + "([က-အ])ႋ"),
            s: "င်္$1ိ"
        }, {
            p: RegExp("^" + "([က-အ])ႌ"),
            s: "င်္$1ီ"
        }, {
            p: RegExp("^" + "([က-အ])ႍ"),
            s: "င်္$1ံ"
        }, {
            p: RegExp("^" + "([က-အ])်ဳႋ"),
            s: "င်္$1ျို"
        }, {
            p: RegExp("^" + "([က-အ])်ႋ"),
            s: "င်္$1ျိ"
        }, {
            p: RegExp("^" + "([က-အ])်ႌ"),
            s: "င်္$1ျီ"
        }, {
            p: RegExp("^" + "([က-အ])်ႍ"),
            s: "င်္$1ျံ"
        }, {
            p: RegExp("^" + "([က-အ])်ႎ"),
            s: "$1ျိံ"
        }, {
            p: RegExp("^" + "ႋ"),
            s: "င်္ိ"
        }, {
            p: RegExp("^" + "ႌ"),
            s: "င်္ီ"
        }, {
            p: RegExp("^" + "ႍ"),
            s: "င်္ံ"
        }, {
            p: RegExp("^" + "ၪ"),
            s: "ဥ"
        }, {
            p: RegExp("^" + "ၫ"),
            s: "ည"
        }, {
            p: RegExp("^" + "ႏ"),
            s: "န"
        }, {
            p: RegExp("^" + "႐"),
            s: "ရ"
        }, {
            p: RegExp("^" + "ႆ"),
            s: "ဿ"
        }, {
            p: RegExp("^" + "[|်ၽ]"),
            s: "ျ"
        }, {
            p: RegExp("^" + "([ျၾ-ႄ])+"),
            s: "ြ"
        }, {
            p: RegExp("^" + "ြ*ႊ"),
            s: "ွှ"
        }, {
            p: RegExp("^" + "ြ"),
            s: "ွ"
        }, {
            p: RegExp("^" + "[|ွႇ]"),
            s: "ှ"
        }, {
            p: RegExp("^" + "ႈ"),
            s: "ှု"
        }, {
            p: RegExp("^" + "ႉ"),
            s: "ှူ"
        }, {
            p: RegExp("^" + "ဳ"),
            s: "ု"
        }, {
            p: RegExp("^" + "ဴ"),
            s: "ူ"
        }, {
            p: RegExp("^" + "္"),
            s: "်"
        }, {
            p: RegExp("^" + "[႔႕]"),
            s: "့"
        }, {
            p: RegExp("^" + "ဥၡ"),
            s: "ဉ္ခ"
        }, {
            p: RegExp("^" + "ဥၢ"),
            s: "ဉ္ဂ"
        }, {
            p: RegExp("^" + "ဥၥ"),
            s: "ဉ္စ"
        }, {
            p: RegExp("^" + "ဥၨ"),
            s: "ဉ္ဇ"
        }, {
            p: RegExp("^" + "ဥၶ"),
            s: "ဉ္ဓ"
        }, {
            p: RegExp("^" + "ဥၸ"),
            s: "ဉ္ပ"
        }, {
            p: RegExp("^" + "ဥၺ"),
            s: "ဉ္ဗ"
        }, {
            p: RegExp("^" + "ဥၹ"),
            s: "ဉ္ဖ"
        }, {
            p: RegExp("^" + "ၚ"),
            s: "ါ်"
        }, {
            p: RegExp("^" + "ၠ"),
            s: "္က"
        }, {
            p: RegExp("^" + "ၡ"),
            s: "္ခ"
        }, {
            p: RegExp("^" + "ၢ"),
            s: "္ဂ"
        }, {
            p: RegExp("^" + "ၣ"),
            s: "္ဃ"
        }, {
            p: RegExp("^" + "ၥ"),
            s: "္စ"
        }, {
            p: RegExp("^" + "[ၦၧ]"),
            s: "္ဆ"
        }, {
            p: RegExp("^" + "ၨ"),
            s: "္ဇ"
        }, {
            p: RegExp("^" + "ၩ"),
            s: "္ဈ"
        }, {
            p: RegExp("^" + "ၬ"),
            s: "္ဋ"
        }, {
            p: RegExp("^" + "ၭ"),
            s: "္ဌ"
        }, {
            p: RegExp("^" + "ၰ"),
            s: "္ဏ"
        }, {
            p: RegExp("^" + "[ၱၲ]"),
            s: "္တ"
        }, {
            p: RegExp("^" + "႖"),
            s: "္တွ"
        }, {
            p: RegExp("^" + "[ၳၴ]"),
            s: "္ထ"
        }, {
            p: RegExp("^" + "ၵ"),
            s: "္ဒ"
        }, {
            p: RegExp("^" + "ၶ"),
            s: "္ဓ"
        }, {
            p: RegExp("^" + "ၷ"),
            s: "္န"
        }, {
            p: RegExp("^" + "ၸ"),
            s: "္ပ"
        }, {
            p: RegExp("^" + "ၹ"),
            s: "္ဖ"
        }, {
            p: RegExp("^" + "ၺ"),
            s: "္ဗ"
        }, {
            p: RegExp("^" + "[ၻ႓]"),
            s: "္ဘ"
        }, {
            p: RegExp("^" + "ၼ"),
            s: "္မ"
        }, {
            p: RegExp("^" + "ႅ"),
            s: "္လ"
        }, {
            p: RegExp("^" + "ႎ"),
            s: "ိံ"
        }, {
            p: RegExp("^" + "[ၮ႑]"),
            s: "ဍ္ဍ"
        }, {
            p: RegExp("^" + "ၯ"),
            s: "ဍ္ဎ"
        }, {
            p: RegExp("^" + "႒"),
            s: "ဋ္ဌ"
        }, {
            p: RegExp("^" + "႗"),
            s: "ဋ္ဋ"
        }, {
            p: RegExp("^" + "၎"),
            s: "၎င်း"
        } ];
        var rules1 = [ {
            p: RegExp("^" + "([    -‍⁠  　\ufeff])့"),
            s: "့$1"
        }, {
            p: RegExp("^" + "([    -‍⁠  　\ufeff]+)([ါ-ူဲ-ျွှ])"),
            s: "$2"
        }, {
            p: RegExp("^" + "့+"),
            s: "့"
        }, {
            p: RegExp("^" + "ေ+င်္([က-အ])"),
            s: "င်္$1ေ"
        }, {
            p: RegExp("^" + "ေ+့+([က-အ])"),
            s: "$1ေ့"
        }, {
            p: RegExp("^" + "ေ+ြ([က-အ])"),
            s: "$1ြေ"
        }, {
            p: RegExp("^" + "ေ+([က-အ])([ျ-ှ]+)"),
            s: "$1$2ေ"
        }, {
            p: RegExp("^" + "ေ+([က-ဪ])"),
            s: "$1ေ"
        } ];
        var rules2 = [ {
            p: RegExp("^" + "ျ်"),
            s: "်ျ"
        }, {
            p: RegExp("^" + "၀([^၀-၉])"),
            s: "ဝ$1",
            matchOnStart: "true"
        }, {
            p: RegExp("^" + "([ါ-ဿ])၀([^၀-၉])"),
            s: "$1ဝ$2"
        }, {
            p: RegExp("^" + "၄([^၀-၉])"),
            s: "၎$1",
            matchOnStart: "true",
            revisit: 0
        }, {
            p: RegExp("^" + "([ါ-ဿ])၄([^၀-၉])"),
            s: "$1၎$2"
        }, {
            p: RegExp("^" + "ဦ"),
            s: "ဦ"
        }, {
            p: RegExp("^" + "့်"),
            s: "့်"
        }, {
            p: RegExp("^" + "ံ([ျ-ှ]*)([ါ-ူဲ]+)"),
            s: "$1$2ံ"
        }, {
            p: RegExp("^" + "([ါာုူ])([ိီဲ])"),
            s: "$2$1"
        }, {
            p: RegExp("^" + "ြ([က-အ])"),
            s: "$1ြ"
        }, {
            p: RegExp("^" + "စျ"),
            s: "ဈ"
        } ];
        var rules3 = [ {
            p: RegExp("^" + "([ျ-ှ])္([က-အ])"),
            s: "္$2$1"
        }, {
            p: RegExp("^" + "ြ်္([က-အ])"),
            s: "်္$1ြ"
        }, {
            p: RegExp("^" + "ံ([ျ-ှ]+)"),
            s: "$1ံ"
        } ];
        var rules4 = [ {
            p: RegExp("^" + "([ြ-ှ]+)ျ"),
            s: "ျ$1"
        }, {
            p: RegExp("^" + "([ွှ]+)ြ"),
            s: "ြ$1"
        }, {
            p: RegExp("^" + "ှွ"),
            s: "ွှ"
        }, {
            p: RegExp("^" + "([ေ]+)([ါ-ူဲ]*)္([က-အ])"),
            s: "္$3$1$2"
        }, {
            p: RegExp("^" + "([ါ-ူဲ]+)္([က-အ])"),
            s: "္$2$1"
        }, {
            p: RegExp("^" + "([ျ-ှ]*)([ေ]+)([ျ-ှ]*)"),
            s: "$1$3$2"
        }, {
            p: RegExp("^" + "့([ိ-ူဲံျ-ှ]+)"),
            s: "$1့"
        }, {
            p: RegExp("^" + "([ါ-ူဲ]+)([ျ-ှ]+)"),
            s: "$2$1"
        }, {
            p: RegExp("^" + "([က-အ])([ါ-ဲံျ-ှ])်([က-အ])"),
            s: "$1်$2$3"
        } ];
        var rules5 = [ {
            p: RegExp("^" + "([ါ-ဲ])([ျ-ှ])"),
            s: "$2$1"
        }, {
            p: RegExp("^" + "([ြ-ှ])ျ"),
            s: "ျ$1"
        }, {
            p: RegExp("^" + "([ွှ])ြ"),
            s: "ြ$1"
        }, {
            p: RegExp("^" + "ှွ"),
            s: "ွှ"
        }, {
            p: RegExp("^" + "း([36uါ-ူဲ့်-ဿ])"),
            s: "$1း"
        }, {
            p: RegExp("^" + "ံု"),
            s: "ုံ"
        } ];
        var rules6 = [ {
            p: RegExp("^" + "ိိ+"),
            s: "ိ"
        }, {
            p: RegExp("^" + "ီီ+"),
            s: "ီ"
        }, {
            p: RegExp("^" + "ုု+"),
            s: "ု"
        }, {
            p: RegExp("^" + "ူူ+"),
            s: "ူ"
        }, {
            p: RegExp("^" + "ဲဲ+"),
            s: "ဲ"
        }, {
            p: RegExp("^" + "ဳဳ+"),
            s: "ဳ"
        }, {
            p: RegExp("^" + "ဵဵ+"),
            s: "ဵ"
        }, {
            p: RegExp("^" + "ံံ+"),
            s: "ံ"
        }, {
            p: RegExp("^" + "့့+"),
            s: "့"
        }, {
            p: RegExp("^" + "္္+"),
            s: "္"
        }, {
            p: RegExp("^" + "််+"),
            s: "်"
        }, {
            p: RegExp("^" + "ျျ+"),
            s: "ျ"
        }, {
            p: RegExp("^" + "ြြ+"),
            s: "ြ"
        }, {
            p: RegExp("^" + "ွွ+"),
            s: "ွ"
        }, {
            p: RegExp("^" + "ှှ+"),
            s: "ှ"
        }, {
            p: RegExp("^" + "ု[ူ်]"),
            s: "ု"
        }, {
            p: RegExp("^" + "ိီ"),
            s: "ီ"
        }, {
            p: RegExp("^" + "[    -‍⁠  　\ufeff]+([ါ-ဲံ-ှ])"),
            s: "$1"
        } ];
        return [ rules0, rules1, rules2, rules3, rules4, rules5, rules6 ];
    }
    function getAllRulesU2Z() {
        var rules0 = [ {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ျ"),
            s: "$1်ၤ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ိံ"),
            s: "$1ႎ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ိ"),
            s: "$1ႋ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ီ"),
            s: "$1ႌ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ံ"),
            s: "$1ႍ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ေ"),
            s: "$1ေၤ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ျို"),
            s: "$1်ဳႋ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ျိ"),
            s: "$1်ႋ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ျီု"),
            s: "$1်ႌဳ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ျီ"),
            s: "$1်ႌ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ျံ"),
            s: "$1်ႍ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])ြ"),
            s: "$1ျၤ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္ိ"),
            s: "ႋ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္ီ"),
            s: "ႌ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္ံ"),
            s: "ႍ"
        }, {
            p: RegExp("^" + "[ငရၚ]်္([က-အ])"),
            s: "$1ၤ"
        }, {
            p: RegExp("^" + "ဥ([ါ-ူဲ])း"),
            s: "ၪ$1း"
        }, {
            p: RegExp("^" + "ဥုံ"),
            s: "ဥံဳ"
        }, {
            p: RegExp("^" + "ိံ"),
            s: "ႎ"
        }, {
            p: RegExp("^" + "ွှ"),
            s: "ႊ"
        }, {
            p: RegExp("^" + "ှု"),
            s: "ႈ"
        }, {
            p: RegExp("^" + "ှူ"),
            s: "ႉ"
        }, {
            p: RegExp("^" + "်"),
            s: "္"
        }, {
            p: RegExp("^" + "ျ"),
            s: "်"
        }, {
            p: RegExp("^" + "ြ"),
            s: "ျ"
        }, {
            p: RegExp("^" + "ွ"),
            s: "ြ"
        }, {
            p: RegExp("^" + "ှ"),
            s: "ွ"
        }, {
            p: RegExp("^" + "ဿ"),
            s: "ႆ"
        }, {
            p: RegExp("^" + "([မ])ှူ"),
            s: "$1ွဴ"
        }, {
            p: RegExp("^" + "ါ်"),
            s: "ၚ"
        }, {
            p: RegExp("^" + "္တွ"),
            s: "႖"
        }, {
            p: RegExp("^" + "္က"),
            s: "ၠ"
        }, {
            p: RegExp("^" + "္ခ"),
            s: "ၡ"
        }, {
            p: RegExp("^" + "္ဂ"),
            s: "ၢ"
        }, {
            p: RegExp("^" + "္ဃ"),
            s: "ၣ"
        }, {
            p: RegExp("^" + "္စ"),
            s: "ၥ"
        }, {
            p: RegExp("^" + "္ဆ"),
            s: "ၧ"
        }, {
            p: RegExp("^" + "္ဇ"),
            s: "ၨ"
        }, {
            p: RegExp("^" + "္ဈ"),
            s: "ၩ"
        }, {
            p: RegExp("^" + "္ဋ"),
            s: "ၬ"
        }, {
            p: RegExp("^" + "္ဌ"),
            s: "ၭ"
        }, {
            p: RegExp("^" + "္ဍ"),
            s: "ၮ"
        }, {
            p: RegExp("^" + "ဍ္ဎ"),
            s: "ၯ"
        }, {
            p: RegExp("^" + "္ဎ"),
            s: "ၯ"
        }, {
            p: RegExp("^" + "္ဏ"),
            s: "ၰ"
        }, {
            p: RegExp("^" + "္တ"),
            s: "ၲ"
        }, {
            p: RegExp("^" + "္ထ"),
            s: "ၴ"
        }, {
            p: RegExp("^" + "္ဒ"),
            s: "ၵ"
        }, {
            p: RegExp("^" + "္ဓ"),
            s: "ၶ"
        }, {
            p: RegExp("^" + "္န"),
            s: "ၷ"
        }, {
            p: RegExp("^" + "္ပ"),
            s: "ၸ"
        }, {
            p: RegExp("^" + "္ဖ"),
            s: "ၹ"
        }, {
            p: RegExp("^" + "္ဗ"),
            s: "ၺ"
        }, {
            p: RegExp("^" + "္ဘ"),
            s: "႓"
        }, {
            p: RegExp("^" + "္မ"),
            s: "ၼ"
        }, {
            p: RegExp("^" + "္လ"),
            s: "ႅ"
        }, {
            p: RegExp("^" + "ဏ္ဍ"),
            s: "႑"
        }, {
            p: RegExp("^" + "ဋ္ဌ"),
            s: "႒"
        }, {
            p: RegExp("^" + "ဋ္ဋ"),
            s: "႗"
        }, {
            p: RegExp("^" + "၎င်း"),
            s: "၎"
        } ];
        var rules1 = [ {
            p: RegExp("^" + "([က-အ])ျေ"),
            s: "ေျ$1"
        }, {
            p: RegExp("^" + "([က-အ])ျ"),
            s: "ျ$1"
        }, {
            p: RegExp("^" + "([က-အ])ွေ့"),
            s: "ေ$1႔ွ"
        }, {
            p: RegExp("^" + "([က-အ])ၤျ"),
            s: "ျ$1ၤ"
        }, {
            p: RegExp("^" + "([က-အ])([်ြွ])ေ"),
            s: "ေ$1$2"
        }, {
            p: RegExp("^" + "([က-ဪ])ေ"),
            s: "ေ$1"
        }, {
            p: RegExp("^" + "န([ၠ-ၨၬၭၰ-ၼႅ႓႖])"),
            s: "ႏ$1"
        }, {
            p: RegExp("^" + "န([ုူ့်ြွႇ-ႊ])([ိီဲံ္ွှၤ])့"),
            s: "ႏ$1$2႔"
        }, {
            p: RegExp("^" + "န([ိီဲံ္ွှၤ])([ုူ့်ြွႇ-ႊ])့"),
            s: "ႏ$1$2႔"
        }, {
            p: RegExp("^" + "န([ိီဲံ္ွှၤ])့"),
            s: "န$1႔"
        }, {
            p: RegExp("^" + "နဲ့"),
            s: "နဲ႔"
        }, {
            p: RegExp("^" + "န့"),
            s: "န႔"
        }, {
            p: RegExp("^" + "နဲ([ုူ့်ြွႇ-ႊ])့"),
            s: "ႏ$1ဲ႔"
        }, {
            p: RegExp("^" + "န([ိီဲံ္ွှၤ])([ုူ့်ြွႇ-ႊ])"),
            s: "ႏ$1$2"
        }, {
            p: RegExp("^" + "န([ုူ့်ြွႇ-ႊ])([ိီဲံ္ွှၤ])"),
            s: "ႏ$1$2"
        }, {
            p: RegExp("^" + "န([ုူ့်ြွႇ-ႊ])့"),
            s: "ႏ$1႔"
        }, {
            p: RegExp("^" + "န([ုူ့်ြွႇ-ႊ])"),
            s: "ႏ$1"
        }, {
            p: RegExp("^" + "([ုူ့်ြွႇ-ႊ])([ိီဲံ္ွှၤ]*)့"),
            s: "$1$2႔"
        }, {
            p: RegExp("^" + "([^၀-၉])၀([ါ-ဿ])"),
            s: "$1ဝ$2"
        }, {
            p: RegExp("^" + "ေ၀([^၀-၉])"),
            s: "ေဝ$1"
        }, {
            p: RegExp("^" + "ဦ"),
            s: "ဦ"
        }, {
            p: RegExp("^" + "့်"),
            s: "့်"
        }, {
            p: RegExp("^" + "([ါာုူ])([ိီဲ])"),
            s: "$2$1"
        }, {
            p: RegExp("^" + "([ျၾ-ႄ])([က-အ])ု"),
            s: "$1$2ဳ"
        } ];
        var rules2 = [ {
            p: RegExp("^" + "ြ႔"),
            s: "ြ႕"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ခဂငစဇဋ-ဎဒဓပ-ဗမဝဠဥဦ])ိွု"),
            s: "ၿ$1ိႇႃ"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ကဃဆဉညဏ-ထဘလသဟအ])ိွု"),
            s: "ႀ$1ိႇႃ"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ခဂငစဇဋ-ဎဒဓပ-ဗမဝဠဥဦ])([ုူ့်ြွႇ-ႊ])([ိီဲံ္ွှၤ])"),
            s: "ႃ$1$2$3"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ကဃဆဉညဏ-ထဘလသဟအ])([ုူ့်ြွႇ-ႊ])([ိီဲံ္ွှၤ])"),
            s: "ႄ$1$2$3"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ခဂငစဇဋ-ဎဒဓပ-ဗမဝဠဥဦ])([ိီဲံ္ွှၤ])"),
            s: "ၿ$1$2"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ကဃဆဉညဏ-ထဘလသဟအ])([ိီဲံ္ွှၤ])"),
            s: "ႀ$1$2"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ခဂငစဇဋ-ဎဒဓပ-ဗမဝဠဥဦ])ူ"),
            s: "ျ$1ဴ"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ကဃဆဉညဏ-ထဘလသဟအ])ူ"),
            s: "ၾ$1ဴ"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ခဂငစဇဋ-ဎဒဓပ-ဗမဝဠဥဦ])(ု)"),
            s: "ျ$1ဳ"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ကဃဆဉညဏ-ထဘလသဟအ])(ု)"),
            s: "ၾ$1ဳ"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ခဂငစဇဋ-ဎဒဓပ-ဗမဝဠဥဦ])([ုူ့်ြွႇ-ႊ])"),
            s: "ႁ$1$2"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ကဃဆဉညဏ-ထဘလသဟအ])([ုူ့်ြွႇ-ႊ])"),
            s: "ႂ$1$2"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ညၫ])"),
            s: "ႂ$1"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ဉၪ])"),
            s: "ျၪ"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ခဂငစဇဋ-ဎဒဓပ-ဗမဝဠဥဦ])"),
            s: "ျ$1"
        }, {
            p: RegExp("^" + "[ျၾ-ႄ]([ကဃဆဉညဏ-ထဘလသဟအ])"),
            s: "ၾ$1"
        }, {
            p: RegExp("^" + "ဉ([ုူ့်ြွႇ-ႊ])"),
            s: "ၪ$1"
        }, {
            p: RegExp("^" + "ည([ုူ့်ြွႇ-ႊ])"),
            s: "ၫ$1"
        }, {
            p: RegExp("^" + "ွိ"),
            s: "ိွ"
        }, {
            p: RegExp("^" + "်([ိီဲံ္ွှၤ])ု[့႔႕]"),
            s: "်$1ဳ႕"
        }, {
            p: RegExp("^" + "်ု[့႔႕]"),
            s: "်ဳ႕"
        }, {
            p: RegExp("^" + "်ု"),
            s: "်ဳ"
        }, {
            p: RegExp("^" + "ၤီ"),
            s: "ႌ"
        } ];
        var rules3 = [ {
            p: RegExp("^" + "([ြ-ှ]+)ျ"),
            s: "ျ$1"
        }, {
            p: RegExp("^" + "([ွှ]+)ြ"),
            s: "ြ$1"
        }, {
            p: RegExp("^" + "ှွ"),
            s: "ွှ"
        }, {
            p: RegExp("^" + "့([ိ-ူဲံ])"),
            s: "$1့"
        }, {
            p: RegExp("^" + "([က-အ])([ါ-ဲံျ-ှ])်([က-အ])"),
            s: "$1်$2$3"
        }, {
            p: RegExp("^" + "ွု"),
            s: "ႈ"
        }, {
            p: RegExp("^" + "ဳ႔"),
            s: "ဳ႕"
        }, {
            p: RegExp("^" + "([ျၾ-ႄ])([က-အ])([ိီဲံ္ွှၤ])ု"),
            s: "$1$2$3ဳ"
        } ];
        var rules4 = [ {
            p: RegExp("^" + "([ွှ])ြ"),
            s: "ြ$1"
        }, {
            p: RegExp("^" + "ှွ"),
            s: "ွှ"
        }, {
            p: RegExp("^" + "း([ါ-ူဲြ-ဿ])"),
            s: "$1း"
        }, {
            p: RegExp("^" + "း([ံ့်])"),
            s: "$1း"
        }, {
            p: RegExp("^" + "ံု"),
            s: "ုံ"
        }, {
            p: RegExp("^" + "်([ၤႋ-ႎ])ို"),
            s: "်$1ိဳ"
        }, {
            p: RegExp("^" + "်ို"),
            s: "်ိဳ"
        } ];
        var rules5 = [ {
            p: RegExp("^" + "([က-အ])ျ်"),
            s: "$1်ျ"
        }, {
            p: RegExp("^" + "([ြ-ှ])ျ"),
            s: "ျ$1"
        }, {
            p: RegExp("^" + "([ွှ])ြ"),
            s: "ြ$1"
        }, {
            p: RegExp("^" + "ှွ"),
            s: "ွှ"
        }, {
            p: RegExp("^" + "([ိ-ူဲ])်([က-အ])်"),
            s: "$1$2်"
        }, {
            p: RegExp("^" + "ိ်"),
            s: "ိ"
        }, {
            p: RegExp("^" + "ီ်"),
            s: "ီ"
        }, {
            p: RegExp("^" + "ု်"),
            s: "ု"
        }, {
            p: RegExp("^" + "ိီ"),
            s: "ီ"
        }, {
            p: RegExp("^" + "ုူ"),
            s: "ု"
        }, {
            p: RegExp("^" + "ါါ+"),
            s: "ါ"
        }, {
            p: RegExp("^" + "ာာ+"),
            s: "ာ"
        }, {
            p: RegExp("^" + "ိိ+"),
            s: "ိ"
        }, {
            p: RegExp("^" + "ီီ+"),
            s: "ီ"
        }, {
            p: RegExp("^" + "ုု+"),
            s: "ု"
        }, {
            p: RegExp("^" + "ူူ+"),
            s: "ူ"
        }, {
            p: RegExp("^" + "ေေ+"),
            s: "ေ"
        }, {
            p: RegExp("^" + "ဲဲ+"),
            s: "ဲ"
        }, {
            p: RegExp("^" + "ံံ+"),
            s: "ံ"
        }, {
            p: RegExp("^" + "််+"),
            s: "်"
        }, {
            p: RegExp("^" + "ျျ+"),
            s: "ျ"
        }, {
            p: RegExp("^" + "ြြ+"),
            s: "ြ"
        }, {
            p: RegExp("^" + "ွွ+"),
            s: "ွ"
        }, {
            p: RegExp("^" + "ှှ+"),
            s: "ှ"
        }, {
            p: RegExp("^" + "ုိ"),
            s: "ို"
        }, {
            p: RegExp("^" + "ုံ"),
            s: "ံု"
        }, {
            p: RegExp("^" + "့္"),
            s: "့္"
        }, {
            p: RegExp("^" + "ြဲ"),
            s: "ဲြ"
        }, {
            p: RegExp("^" + "ြီ"),
            s: "ီြ"
        }, {
            p: RegExp("^" + "ွႈ"),
            s: "ႈ"
        } ];
        return [ rules0, rules1, rules2, rules3, rules4, rules5 ];
    }
    function getAllRulesZNorm() {
        var rules0 = [ {
            p: RegExp("^" + "ဦ"),
            s: "ဦ"
        }, {
            p: RegExp("^" + "ု([ိံ])"),
            s: "$1ု"
        }, {
            p: RegExp("^" + "္([့႔႕])"),
            s: "$1္"
        }, {
            p: RegExp("^" + "ြ([ီဲ])"),
            s: "$1ြ"
        }, {
            p: RegExp("^" + "ဳိ"),
            s: "ိဳ"
        }, {
            p: RegExp("^" + "ွိ"),
            s: "ိွ"
        }, {
            p: RegExp("^" + "ႉ"),
            s: "ွဴ"
        }, {
            p: RegExp("^" + "ၤ်"),
            s: "်ၤ"
        }, {
            p: RegExp("^" + "ၧ"),
            s: "ၦ"
        }, {
            p: RegExp("^" + "ၲ"),
            s: "ၱ"
        }, {
            p: RegExp("^" + "ၴ"),
            s: "ၳ"
        }, {
            p: RegExp("^" + "႓"),
            s: "ၻ"
        } ];
        var rules1 = [ {
            p: RegExp("^" + "ိ+"),
            s: "ိ"
        }, {
            p: RegExp("^" + "ီ+"),
            s: "ီ"
        }, {
            p: RegExp("^" + "ု+"),
            s: "ု"
        }, {
            p: RegExp("^" + "ူ+"),
            s: "ူ"
        }, {
            p: RegExp("^" + "ဲ+"),
            s: "ဲ"
        }, {
            p: RegExp("^" + "ဳ+"),
            s: "ဳ"
        }, {
            p: RegExp("^" + "ဴ+"),
            s: "ဴ"
        }, {
            p: RegExp("^" + "ံ+"),
            s: "ံ"
        }, {
            p: RegExp("^" + "့+"),
            s: "့"
        }, {
            p: RegExp("^" + "္+"),
            s: "္"
        }, {
            p: RegExp("^" + "်+"),
            s: "်"
        }, {
            p: RegExp("^" + "ျ+"),
            s: "ျ"
        }, {
            p: RegExp("^" + "ြ+"),
            s: "ြ"
        }, {
            p: RegExp("^" + "ွ+"),
            s: "ွ"
        }, {
            p: RegExp("^" + "ှ+"),
            s: "ွ"
        } ];
        var rules2 = [ {
            p: RegExp("^" + "[့႔႕]+"),
            s: "့"
        }, {
            p: RegExp("^" + "စ်"),
            s: "ဈ"
        }, {
            p: RegExp("^" + "ဝ"),
            s: "၀"
        }, {
            p: RegExp("^" + "ုႈ"),
            s: "ႈ"
        }, {
            p: RegExp("^" + "ျ်"),
            s: "်ျ"
        }, {
            p: RegExp("^" + "ွု"),
            s: "ႈ"
        }, {
            p: RegExp("^" + "ွႈ"),
            s: "ႈ"
        }, {
            p: RegExp("^" + "ျ([က-အ])ျ$"),
            s: "ျ$1"
        } ];
        var rules3 = [ {
            p: RegExp("^" + "[ျၾ-ႄ]+"),
            s: "ျ"
        } ];
        var rules4 = [ {
            p: RegExp("^" + "([ျၾ-ႄ])([က-အ])ံု"),
            s: "$1$2ဳံ"
        } ];
        var rules5 = [ {
            p: RegExp("^" + "ဳ"),
            s: "ု"
        } ];
        var rules6 = [ {
            p: RegExp("^" + "ံု"),
            s: "ုံ"
        }, {
            p: RegExp("^" + "့့္"),
            s: "့္"
        }, {
            p: RegExp("^" + "[|ၪၫ]"),
            s: "ည"
        } ];
        var rules7 = [ {
            p: RegExp("^" + "[    -‍⁠  　\ufeff]+([က-႟])"),
            s: "$1",
            revisit: 0
        } ];
        return [ rules0, rules1, rules2, rules3, rules4, rules5, rules6, rules7 ];
    }
    var ZawgyiConverter = function() {
        function ZawgyiConverter() {}
        ZawgyiConverter.prototype.zawgyiToUnicode = function(inString) {
            return runAllPhases(getAllRulesZ2U(), inString);
        };
        ZawgyiConverter.prototype.unicodeToZawgyi = function(inString) {
            return runAllPhases(getAllRulesU2Z(), inString);
        };
        ZawgyiConverter.prototype.normalizeZawgyi = function(inString) {
            return runAllPhases(getAllRulesZNorm(), inString);
        };
        return ZawgyiConverter;
    }();
    exports.ZawgyiConverter = ZawgyiConverter;
})(typeof google_myanmar_tools == "undefined" ? google_myanmar_tools = {} : google_myanmar_tools);