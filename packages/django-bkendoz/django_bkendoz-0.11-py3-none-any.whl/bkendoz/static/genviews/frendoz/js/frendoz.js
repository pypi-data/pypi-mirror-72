/* namespace cmd {{{1 */
var cmd = new function() 
{
    // CSS{{{
    var _getStylePath = function () {
        var mainCss = "frendoz.css";
        var path = ""
        document.querySelectorAll("link").forEach(link => {
            if (link.href.includes(mainCss)) {
                path = link.href.split(mainCss)[0];
                return;
            }
        })
        return path;
    }

    var _replaceCharsInPage = function(charsDict) { 
        if (!charsDict) return;

        document.querySelectorAll("body, body *").forEach(node =>  {
            if (node.children.length != 0) return;
            var elToScan = ["span", "p", "a", "h1", "h2", "h3"];
            if (!elToScan.includes(node.localName)) return;

            Object.keys(charsDict).forEach(oldC => {
                var regex = new RegExp(oldC, 'g');
                node.innerHTML = node.innerHTML.replace(regex, charsDict[oldC]);
            });
        })
    }

    this.resetTheme = function(css_name, replaceChars=null) {
        document.querySelectorAll("link").forEach(link => {
            if (link.href.includes("variants")) {
                link.remove();
            }
        });
        _replaceCharsInPage(replaceChars);
    }

    this.changeTheme = function(theme, replaceChars=null) {
        var path = _getStylePath();
        if (!path) return;

        var themePath = path + "variants/" + theme + ".css";
        var head = document.getElementsByTagName("head")[0];
        head.insertAdjacentHTML("beforeend",
            "<link rel='stylesheet' href='" + themePath + "' />");

        _replaceCharsInPage(replaceChars);
    }
    //}}}
    // redirect {{{
    this.go = function(url) {
        location.href = url;
    }

    this.toDetail = this.go;
    this.toList = this.go;
    //}}}
}

/* ajax {{{1 */

function ajaxGet(url, handler) {
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400)  {
            handler(JSON.parse(this.response));
        } else  {
        }
    };
    request.onerror = function() {
    };
    request.send();
}

function ajaxPost(eleme, url, handler, data, 
    contentType = "application/json") {
    var request = new XMLHttpRequest();
    request.open("POST", url, true);
    request.setRequestHeader("Content-type", contentType);
    request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    request.onload = function() {
        if (this.status >= 200 && this.status <= 202) {
            handler(element, this.status, JSON.parse(this.response));
        }
    };
    request.onerror = function() {};
    request.send(data);
}

function drfHydrateSelect(select, results) {
    var index = 0;
    for (index in results) {
        select.options[index] = new Option(results[index].name, results[index].id);
        index++;
    }
}

function drfGetDataForSelect(elementId, url) {
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.onload = function() {
        if (this.status >= 200 && this.status < 400)  {
            var select = document.getElementById(elementId);
            var data = JSON.parse(this.response);

            resetSelect(select);
            drfHydrateSelect(select, data.results);
        } else  {
        }
    };
    request.onerror = function() {
    };
    request.send();
}

async function getDataFromUrls(urls = null) {
    const promiseData = Promise.all(
        urls.map(url =>
            fetch(url)
            .then(checkStatus)
            .then(parseJSON)
        )
    ).then(data => {
        var objectList = [];
        data.forEach(data_type => {
            data_type.forEach(object => {
                objectList.push(object);
            });
        });
        return objectList;
    });

    var result = await promiseData.then(function(response) {
        return response;
    });
    return result;

    function checkStatus(response) {
        if (response.ok)  {
            return Promise.resolve(response);
        } else  {
            return Promise.reject(new Error(response.statusText));
        }
    }

    function parseJSON(response) {
        return response.json();
    }
}

/* general tools {{{1 */
function resetSelect(select)  {
    var totalOptions = select.options.length;
    for (var i = totalOptions; i >= 0; i--) {
        if (select.options[i]) select.remove(i);
    }
}

function getCookie (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++)  {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=")  {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function baseClamp(number, lower, upper) {
    if (number === number) {
        if (upper !== undefined)  {
            number = number <= upper ? number : upper;
        }
        if (lower !== undefined)  {
            number = number >= lower ? number : lower;
        }
    }
    return number;
}

// association evenements, action {{{1
function setToggleMenuEvents() {
    var menuToggle = document.querySelector("#btn-menu-toggle"); 
    if (menuToggle) menuToggle.addEventListener("click", toggleMenuVisibility);
}

function setModalEvents() {
    var modalLinks = document.querySelectorAll(".modal-open");
    modalLinks.forEach(a => { a.addEventListener("click", openModal)});

    var modalClose = document.querySelectorAll(".modal-close");
    modalClose.forEach(cl => { cl.addEventListener("click", closeModal)});
}

function setColorPickerEvents() {
    document.querySelectorAll(".color-select input[name=color]").forEach(input => {
        input.addEventListener("change", colorChosen);
    });
    document.querySelectorAll(".color-select li").forEach(li => {
        li.addEventListener("click", colorPaletteClick);
    });
}

function setListEvents(listSelector) {
    document.querySelectorAll(listSelector).forEach(list => {
        list.querySelectorAll("thead input").forEach(input => {
            input.addEventListener("keyup", function(e) { listInputChange(e, this, list) });
            input.addEventListener("change", function (e) { listInputChange(e, this, list) });
        });

        btnLsSort = list.querySelectorAll("button.btn-ls-sort");
        btnLsSort.forEach(btn => {
            btn.addEventListener("mouseup", function(e) { listSortClick(e, this, list) });
        });

        list.querySelectorAll("button.btn-ls-res").forEach(btn => {
            btn.addEventListener("mouseup", function(e) { listResetInputClick(e, this, list)});
        });
    });
}
//}}}
/* actions sur evenements {{{1 */
// menu toggle {{{
function toggleMenuVisibility() {
    var menu = document.querySelector("menu");
    if (menu.style.display === "flex") {
        menu.style.display = "none";
    } else {
        menu.style.display = "flex";
    }
}//}}}
// color picker {{{
function colorChosen(event) {
    var color_preview = this.parentNode.querySelector(".preview");
    color_preview.style.backgroundColor = this.value;
}

function colorPaletteClick(event) {
    var rootNode = this.parentNode.parentNode;
    var color_field = rootNode.querySelector("input[name=color]");
    color_field.value = this.dataset.hexcolor;
    var color_preview = rootNode.querySelector(".preview");
    color_preview.style.backgroundColor = this.style.backgroundColor;
}
//}}}
// list evenements {{{2 
// list change on input search {{{
function listInputChange(event, inputSearch, list) {
    btnRes = list.querySelector("button[data-res=" + inputSearch.name + "]");
    rows = list.querySelectorAll("tbody tr");
    searchValue = inputSearch.value.toLowerCase();
    if (searchValue == "") {
        btnRes.classList.add("invisible");
        resetSearchFields(rows);
        return;
    }

    btnRes.classList.remove("invisible");
    rows.forEach(row => {
        dataStr = row
            .querySelector("[data-field=" + inputSearch.dataset.search + "]")
            .querySelector(".ls-field");
        dataStr.innerHTML = dataStr.innerText;
        hintedName = addSearchHint(dataStr.innerText, searchValue);

        if (hintedName) {
            dataStr.innerHTML = hintedName;
            row.classList.remove("hidden");
        } 
        else {
            row.classList.add("hidden");
        }
    });
}
//}}}
// list click on btn sort {{{
function listSortClick(event, buttonSort, list)  {
    event.preventDefault();
    event.stopPropagation();
    btnCls = buttonSort.classList;
    iCls = buttonSort.querySelector("i.fa").classList;
    if (btnCls.contains("is-off") && iCls.contains("fa-chevron-circle-down")) {
        btnLsSort.forEach(b => {
            b.classList.remove("is-on");
            b.classList.add("is-off");
            var i = b.querySelector("i.fa");
            i.classList.remove("fa-chevron-circle-up");
            i.classList.add("fa-chevron-circle-down");
        });
        btnCls.remove("is-off");
        btnCls.add("is-on");
        tableSort(list, buttonSort.dataset.sort);
    } 
    else {
        iCls.toggle("fa-chevron-circle-down");
        iCls.toggle("fa-chevron-circle-up");
        reverseList(list);
    }
}
//}}}
// list click on btn reset {{{
function listResetInputClick(event, buttonReset, list) {
    input = list.querySelector("input[name=" + buttonReset.dataset.res + "]");
    input.value = "";
    var event = new Event('change');
    input.dispatchEvent(event);
}
//}}}
// list sort {{{
function tableSort(list, sortby) {
    switching = true;
    while (switching) {
        switching = false;
        rowToSort = list.querySelectorAll("tbody>tr");
        for (i = 0; i < rowToSort.length - 1; i++)  {
            x = rowToSort[i]
                .querySelector("[data-field=" + sortby + "]")
                .querySelector(".ls-field");
            y = rowToSort[i + 1]
                .querySelector("[data-field=" + sortby + "]")
                .querySelector(".ls-field");
            xstr = x.innerHTML.toLowerCase();
            ystr = y.innerHTML.toLowerCase();
            if (xstr > ystr)  {
                rowToSort[i].parentNode.insertBefore(rowToSort[i + 1], rowToSort[i]);
                switching = true;
                break;
            }
        }
    }
}
//}}}
// list reverse sort {{{
function reverseList(list)  {
    tbody = list.querySelector("tbody");
    rows = tbody.querySelectorAll("tr");
    for (var i = 0; i < rows.length; i++) {
        tbody.insertBefore(rows[i], tbody.children[0]);
    }
}
//}}}
// list reset on input value empty {{{
function resetSearchFields(rows)  {
    rows.forEach(row => {
        row.querySelectorAll(".ls-field").forEach(field => {
            field.innerHTML = field.innerText;
        });
        row.classList.remove("hidden");
    });
}
//}}}
// list highlight search {{{
function addSearchHint(str, chars)  {
    started = false;
    found = false;
    if (!str.toLowerCase().includes(chars)) return false;

    hintedName = "";
    for (i=0; i < str.length; i++) {
        if (!found && str[i].toLowerCase() == chars[0].toLowerCase()) {
            found = true;
            tempStr = "<span class='table-search-match'>" + str[i];
            for (j=1; j<chars.length && i+j<str.length; j++) {
                if (str[i+j].toLowerCase() != chars[j].toLowerCase())
                {
                    found=false;
                    break;
                }
                tempStr += str[i + j];
            }

            if (found) {
                tempStr += "</span>";
                hintedName += tempStr;
                i+=j-1;
            } 
            else {
                hintedName += str[i];
            }
        }
        else {
            hintedName += str[i];
        }
        {
        }
        return hintedName;
    }
}
//}}}

/* autoComplete {{{1 */
// default behaviours {{{2 
function _defaultSelectionHandler(feedback, input, dispKeys) {
    input.value = feedback.selection.value[dispKeys[0]];
    console.log(input);

}

function _defaultDisplayResult(data, source, dispKeys) {
    source.innerHTML = "<div class='autoComplete_match'>" 
        + data.match
        + "</div>";
}
//}}}
// createAutoComplete {{{2 */
function createAutoComplete(ph, qsRootAutoC, dataUrl, 
    dispKeys=['name'], matchKeys=['name'], maxResults=10,
    displayResult=_defaultDisplayResult, selectionHandler=_defaultSelectionHandler) {
    // init {{{
    var elRootAutoC = document.querySelector(qsRootAutoC);
    if (elRootAutoC == null) return;

    var qsInpAutoC = qsRootAutoC + " input";
    var elInpAutoC = document.querySelector(qsInpAutoC);
    if (elInpAutoC == null) return;

    var qsListAutoC = qsRootAutoC + " div.autoComplete_list";
    var elBtnReset = elRootAutoC.querySelector("button");

    elInpAutoC.addEventListener("keydown", _captureAutoCKeys);
    elInpAutoC.addEventListener("autoComplete", _watchAutoCValue);
    elInpAutoC.addEventListener("focusin", _focusInAutoC);
    elInpAutoC.addEventListener("focusout", _focusOutAutoC);
    elBtnReset.addEventListener("click", _resetAutoC);
    //}}}
    // set autoC {{{3
    const autoCompletejs = new autoComplete( {
        data: {
            src: _queryAutoCData ,            
            key: matchKeys,
        },
        // params {{{
        selector: qsInpAutoC,
        placeHolder: ph,
        trigger: {
            event: ["focusin", "focusout", "input"]
        },
        searchEngine: "loose",
        maxResults: maxResults,
        highlight: true,
        //}}}
        // result list {{{
        resultsList: {
            render: true,
            container: source =>  {
                source.setAttribute("class", "autoComplete_list");
            },
            destination: elInpAutoC,
            position: "afterend",
            element: "div",
        },
        //}}}
        // result item{{{
        resultItem: {
            element: "div",
            content: (data, source) => {
                displayResult(data, source, dispKeys);
            }
        },
        //}}}

        noResults: _emptyAutoCResults,
        onSelection: function(feedback) { 
            console.log(feedback)
            selectionHandler(feedback, elInpAutoC, dispKeys); 
        }
    });
    //}}}
    // autoC func {{{3
    function _emptyAutoCResults() {
        const result = document.createElement("div");
        result.setAttribute("class", "autoComplete_result");
        result.innerHTML = "Aucun Résultat";
        elRootAutoC.querySelector(qsListAutoC).appendChild(result);
    }

    async function _queryAutoCData() {
        const query = elInpAutoC.value;
        const source = await fetch(dataUrl);
        return await source.json();
    }
    //}}}
    return elInpAutoC;
    // action sur evenements {{{3
    function _watchAutoCValue(ev) {
        if (this.value != "") {
            elBtnReset.classList.add("show-reset");
        }
        else {
            _resetAutoC();
        }
    }

    function _captureAutoCKeys(ev) {
        if (ev.key == "Enter") {
            ev.preventDefault();
            //smthing selected with arrow keys{{{
            var elListAutoC = elRootAutoC.querySelector(qsListAutoC);
            var elSelected = elListAutoC.querySelectorAll(".autoComplete_selected");
            if (elSelected.length > 0) return;
            //}}}
            // action on hover or just enter{{{
            var elToClickOn = null;
            var elHover = elListAutoC.querySelector(".autoComplete_result:hover");
            if (elHover) {
                elToClickOn = elHover;
            }
            else {
                elToClickOn = elListAutoC.children[0];
            }

            elToClickOn.classList.add("autoComplete_selected");
            mousedown = new Event("mousedown");
            elToClickOn.dispatchEvent(mousedown);
            //}}}
        }
        if (ev.key == "Escape") _resetAutoC();
    }

    function _focusInAutoC() {
        elRootAutoC.querySelector(qsListAutoC).hidden = false;
    }

    function _focusOutAutoC() {
        elRootAutoC.querySelector(qsListAutoC).hidden = true;
    }

    function _resetAutoC() {
        elBtnReset.classList.remove("show-reset");
        elInpAutoC.value = "";
        elRootAutoC.querySelector(qsListAutoC).innerHTML = "";
    }
    //}}}
}

//}}}
/* main {{{1 */
setToggleMenuEvents();
