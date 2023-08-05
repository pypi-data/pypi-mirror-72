// command bar {{{
// command bar display options {{{
var dispMapping = {
    "handler": {
        "changeTheme": "Style",
        "resetTheme": "Style",
        "toList": "Liste",
        "toDetail": "Détail",
        "go": "Nav"
    },
    "type": {
        "cmd": '<i class="fa fa-terminal"></i>',
        "cable": '<i class="fa fa-ethernet"></i>',
        "data": '<i class="fa fa-database"></i>',
        "nav": '<i class="fa fa-directions"></i>'
    }
}
//}}}
// command bar display {{{
function commandBarDisplayResult(data, source, dispKeys) {
    var result = "";
    dispKeys.forEach(k => {
        if (k==data.key) {
            result += "<div class='autoComplete_match'>" 
                + data.match
                + "</div>";
        }
        else {
            result += " <div>" 
                + dispMapping[k][data.value[k]] 
                + "</div>";
        }
    });
    source.innerHTML = result
}
//}}}
// command bar selection {{{
function commandBarSelectionHandler(feedback, input) {
    input.value = "";
    //console.log(feedback);
    //console.log(feedback.selection.value);
    const selection = feedback.selection.value;
    var func = "cmd." + selection.handler;
    console.log(selection);
    cmd[selection.handler](selection.param1, selection.param2);
}
//}}}
//command bar create{{{
var omniBar = createAutoComplete(
    "Omnibar Demo",
    "#autoComplete_cmdbar",
    "/demo/cmdbar.json",
    ["type", "handler", "param0"],
    ["param0"],
    8,
    commandBarDisplayResult,
    commandBarSelectionHandler
);
//}}}
//}}}
omniBar.focus();

document.addEventListener("keydown", function(event) {
    if (event.key == "o") {
        var inpWithFocus = document.querySelectorAll("input:focus");
        if (inpWithFocus.length > 0) return;

        omniBar.focus();
        event.stopPropagation();
        event.preventDefault();
    }
});
