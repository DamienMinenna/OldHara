// Edit table of ref with the new data
function edit_table(data) {
    let html
    html = "<td id='appadd'>" + JSON.stringify(data) + "</td>"
    + "<td id='appadd'><a type='button' href='ref/"+ data['id'] + "'><i class='fas fa-share-square'></i></a></td>"
    + "<td id='appadd'></td>"
    + "<td id='appadd'>" + data['listauthor'] + "</td>"
    + "<td id='appadd'>" + data['title'] + "</td>"
    + "<td id='appadd'>" + data['dateY'] + "</td>"
    + "<td id='appadd'>" + data['journal'] + "</td>";
    return html
}

// DISPLAY ref deails when click on a row of the ref table 
$("#idtableref").on('click', 'tr', function()  {

    // GET data (full JSON of the ref)
    var data = $(this).find('td:first-child').text();
    data = JSON.parse(data)

    // REMOVE class table-selected for every one
    var table = document.getElementById("idtableref");
    for (var i = 1, row; row = table.rows[i]; i++) {
        var idTable = table.rows[i].id
        if($('#'+idTable).hasClass("table-selected")){
            $('#'+idTable).removeClass("table-selected")
        }
    }

    // ADD class table-selected for selected
    $("#listRef_"+data.id).addClass("table-selected");

    // MODIFY the right column to include details
    $('#detail_info').html("<a type='button' href='ref/" + data['id'] + "'><i class='fas fa-share-square'></i>");

    if (data['status'] == 1) {

        html_scanit = "<form action='/ref/" + data['id'] + "/' method='POST'>"
        + csrf_token_folder
        + "<input type='hidden' name='scan-file' value='" + data['id'] + "' /><button class='btn btn-success btn-sm' type='submit'>Scan document</button> </form>";

        // $('#detail_scan').html("<span class='detail-names'>Document can be scanned: </span> <a type='button' href='ref/" + data['id'] + "'>Scan it!</i>");
        $('#detail_scan').html("<span class='detail-names'>Document can be scanned: </span>" + html_scanit);

    } else {
        $('#detail_scan').html("");
    }

    $('#detail_folder').html("<div id='id-update-folder' class='detail-editable'>" + data['folder'] + "</div>");
    $('#detail_type').html("<div id='id-update-type' class='detail-editable'>" + data['type'] + "</div>");
    $('#detail_title').html("<div contenteditable='true' id='id-update-title' class='detail-editable'>" + data['title'] + "</div>");
    $('#detail_authors').html("<div contenteditable='true' id='id-update-authors' class='detail-editable'>" + data['listauthor'] + "</div>");
    $('#detail_journal').html("<div contenteditable='true' id='id-update-journal' class='detail-editable'>" + data['journal']+ "</div>");
    $('#detail_dateD').html("<div contenteditable='true' id='id-update-dateD' class='detail-editable'>" + data['dateD']+ "</div>");
    $('#detail_dateM').html("<div id='id-update-dateM' class='detail-editable'>" + data['dateMword'] + "</div>");
    $('#detail_dateY').html("<div contenteditable='true' id='id-update-dateY' class='detail-editable'>" + data['dateY']+ "</div>");
    $('#detail_volume').html("<div contenteditable='true' id='id-update-volume' class='detail-editable'>" + data['volume'] + "</div>");
    $('#detail_issue').html("<div contenteditable='true' id='id-update-issue' class='detail-editable'>" + data['issue'] + "</div>");
    $('#detail_page').html("<div contenteditable='true' id='id-update-page' class='detail-editable'>" + data['page'] + "</div>");
    $('#detail_artnumber').html("<div contenteditable='true' id='id-update-articlenumber' class='detail-editable'>" + data['articlenumber'] + "</div>");

    $('#detail_doi').html("<a target='_blank' href='https://doi.org/" + data['DOI'] + "'>" + data['DOI'] + "</a>");
    $('#detail_badgedimension').html("<span class='__dimensions_badge_embed__' data-doi=" + data['DOI'] + " data-style='small_rectangle'></span>" + "<div data-badge-popover='left' data-link-target='_blank' data-hide-no-mentions='true' data-doi=" + data['DOI'] + " class='altmetric-embed'></div>");
    
    $('#detail_delete').html("<button type='button' class='btn btn-danger btn-sm mb-2' id='id-delete-ref'><span class='fas fa-trash-alt'></span></button>");

    window.__dimensions_embed.addBadges()
    _altmetric_embed_init();


    // Update Title
    document.getElementById("id-update-title").addEventListener("input", function() {
        var newtitle = $('#id-update-title').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'title': newtitle,
            },
            dataType: 'json',
            success: function (responseData) {

                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);

            }
        });
    }, false);

    // Update authors
    document.getElementById("id-update-authors").addEventListener("input", function() {
        var newauthors = $('#id-update-authors').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'listauthor': newauthors,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update journal
    document.getElementById("id-update-journal").addEventListener("input", function() {
        var newjournal = $('#id-update-journal').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'journal': newjournal,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update volume
    document.getElementById("id-update-volume").addEventListener("input", function() {
        var newvolume = $('#id-update-volume').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'volume': newvolume,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update Issue
    document.getElementById("id-update-issue").addEventListener("input", function() {
        var newissue = $('#id-update-issue').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'issue': newissue,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update Page
    document.getElementById("id-update-page").addEventListener("input", function() {
        var newpage = $('#id-update-page').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'page': newpage,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update Article number
    document.getElementById("id-update-articlenumber").addEventListener("input", function() {
        var newarticlenumber = $('#id-update-articlenumber').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'articlenumber': newarticlenumber,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update dateD
    document.getElementById("id-update-dateD").addEventListener("input", function() {
        var newdate = $('#id-update-dateD').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'dateD': newdate,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update dateM
    $( "#id-update-dateM" ).one( "click", function() {
        let html_dateMlist;

        html_dateMlist = "<form action='' method='POST' id='id-selection-dateM_form'>"
            + csrf_token_folder
            + "<select id='id-update-dateM_from_form' name='dateMword' onchange='this.form.submit()'>"
            + "<option value='" + data['dateMword'] + "'>" + data['dateMword'] + "</option>";
        
        for(i = 0; i < month_word.length; i++){
            if(!(month_word[i] == data['dateMword'])){
                html_dateMlist += "<option value='" + month_word[i] + "'>" + month_word[i] + "</option>"
            }
        };

        html_dateMlist += "</select></form>"
        $("#id-update-dateM").html(html_dateMlist);

        $(document).ready(function(e) {
            $("[name='dateMword']").on('change', function() {
                $.ajax({
                    synch: 'true',
                    type: "POST",
                    url: url_update_ref,
                    data: {
                        'id': data['id'],
                        'dateMword': $("#id-update-dateM_from_form").val()
                    },
                    dataType: 'json',
                    success: function(responseData) {
                        let html_table;
                        html_table = edit_table(responseData);
                        $("#listRef_"+data['id']).html(html_table);
                    }
                });
                return false;
            });
        }, false);
    });

    // Update dateY
    document.getElementById("id-update-dateY").addEventListener("input", function() {
        var newdate = $('#id-update-dateY').html();
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'dateY': newdate,
            },
            dataType: 'json',
            success: function (responseData) {
                let html_table;
                html_table = edit_table(responseData);
                $("#listRef_"+data['id']).html(html_table);
            }
        });

    }, false);

    // Update Folder
    $( "#id-update-folder" ).one( "click", function() {
        let html_folderlist;

        html_folderlist = "<form action='' method='POST' id='id-selection-folder_form'>"
            + csrf_token_folder
            + "<select id='id-update-folder_from_form' name='folder' onchange='this.form.submit()'>"
            + "<option value='" + data['folder'] + "'>" + data['folder'] + "</option>";
        
        for(i = 0; i < folder_list.length; i++){
            if(!(folder_list[i] == data['folder'])){
                html_folderlist += "<option value='" + folder_list[i] + "'>" + folder_list[i] + "</option>"
            }
        };

        html_folderlist += "</select></form>"
        $("#id-update-folder").html(html_folderlist);

        $(document).ready(function(e) {
            $("[name='folder']").on('change', function() {
                $.ajax({
                    synch: 'true',
                    type: "POST",
                    url: url_update_ref,
                    data: {
                        'id': data['id'],
                        'folder': $("#id-update-folder_from_form").val()
                    },
                    dataType: 'json',
                    success: function(responseData) {
                        let html_table;
                        html_table = edit_table(responseData);
                        $("#listRef_"+data['id']).html(html_table);
                    }
                });
                return false;
            });
        }, false);
    });


    // Update type
    $( "#id-update-type" ).one( "click", function() {
        let html_typelist;

        html_typelist = "<form action='' method='POST' id='id-selection-type_form'>"
            + csrf_token_folder
            + "<select id='id-update-type_from_form' name='type' onchange='this.form.submit()'>"
            + "<option value='" + data['foltypeder'] + "'>" + data['type'] + "</option>";
        
        for(i = 0; i < type_ref.length; i++){
            if(!(type_ref[i] == data['type'])){
                html_typelist += "<option value='" + type_ref[i] + "'>" + type_ref[i] + "</option>"
            }
        };
    
        html_typelist += "</select></form>"
        $("#id-update-type").html(html_typelist);

        $(document).ready(function(e) {
            $("[name='type']").on('change', function() {
                $.ajax({
                    synch: 'true',
                    type: "POST",
                    url: url_update_ref,
                    data: {
                        'id': data['id'],
                        'type': $("#id-update-type_from_form").val()
                    },
                    dataType: 'json',
                    success: function(responseData) {
                        let html_table;
                        html_table = edit_table(responseData);
                        $("#listRef_"+data['id']).html(html_table);
                    }
                });
                return false;
            });
        }, false);
    });

    // Delete ref
    document.getElementById("id-delete-ref").addEventListener("click", function() {
        var delete_ref = true;
        $.ajax({
            synch: 'true',
            url: url_update_ref,
            type: 'POST',
            data: {
                'id': data['id'],
                'delete_ref': delete_ref,
            },
            dataType: 'json',
            success: function (responseData) {
                window.location.reload()
            }
        });
    }, false);

});


////////////////////////////////////////////////////
// ref-info.html

// Make the progress bar disappear
setTimeout(fade_out, 1500);
function fade_out() {
$("#id-progress-pdf").fadeOut().empty();
}


// GET data (full JSON of the ref)
var data = $("#id-data-selected-ref").text();
data = JSON.parse(data)

// Update Title (Selected ref)
document.getElementById("id-update-selected-title").addEventListener("input", function() {
    var newtitle = $('#id-update-selected-title').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'title': newtitle,
        },
        dataType: 'json',
        success: function (responseData) {
            // let html_table;
            // html_table = edit_table(responseData);
            // $("#listRef_"+data['id']).html(html_table);
        }
    });
}, false);

// Update authors (Selected ref)
document.getElementById("id-update-selected-authors").addEventListener("input", function() {
    var newauthors = $('#id-update-selected-authors').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'listauthor': newauthors,
        },
        dataType: 'json',
        success: function (responseData) {
            // let html_table;
            // html_table = edit_table(responseData);
            // $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);

// Update journal (Selected ref)
document.getElementById("id-update-selected-journal").addEventListener("input", function() {
    var newjournal = $('#id-update-selected-journal').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'journal': newjournal,
        },
        dataType: 'json',
        success: function (responseData) {
            // let html_table;
            // html_table = edit_table(responseData);
            // $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);

// Update volume (Selected ref)
document.getElementById("id-update-selected-volume").addEventListener("input", function() {
    var newvolume = $('#id-update-selected-volume').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'volume': newvolume,
        },
        dataType: 'json',
        success: function (responseData) {
            // let html_table;
            // html_table = edit_table(responseData);
            // $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);

// Update Issue (Selected ref)
document.getElementById("id-update-selected-issue").addEventListener("input", function() {
    var newissue = $('#id-update-selected-issue').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'issue': newissue,
        },
        dataType: 'json',
        success: function (responseData) {
            // let html_table;
            // html_table = edit_table(responseData);
            // $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);

// Update Page
document.getElementById("id-update-selected-page").addEventListener("input", function() {
    var newpage = $('#id-update-selected-page').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'page': newpage,
        },
        dataType: 'json',
        success: function (responseData) {
            // let html_table;
            // html_table = edit_table(responseData);
            // $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);

// Update Article number (Selected ref)
document.getElementById("id-update-selected-articlenumber").addEventListener("input", function() {
    var newarticlenumber = $('#id-update-selected-articlenumber').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'articlenumber': newarticlenumber,
        },
        dataType: 'json',
        success: function (responseData) {
            // let html_table;
            // html_table = edit_table(responseData);
            // $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);

// Update dateD (Selected ref)
document.getElementById("id-update-selected-dateD").addEventListener("input", function() {
    var newdate = $('#id-update-selected-dateD').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'dateD': newdate,
        },
        dataType: 'json',
        success: function (responseData) {
            let html_table;
            html_table = edit_table(responseData);
            $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);

// Update dateM (Selected ref)
$( "#id-update-selected-dateM" ).one( "click", function() {
    let html_dateMlist;

    html_dateMlist = "<form action='' method='POST' id='id-selection-dateM_form'>"
        + csrf_token_folder
        + "<select id='id-update-dateM_from_form' name='dateMword' onchange='this.form.submit()'>"
        + "<option value='" + data['dateMword'] + "'>" + data['dateMword'] + "</option>";
    
    for(i = 0; i < month_word.length; i++){
        if(!(month_word[i] == data['dateMword'])){
            html_dateMlist += "<option value='" + month_word[i] + "'>" + month_word[i] + "</option>"
        }
    };

    html_dateMlist += "</select></form>"
    $("#id-update-selected-dateM").html(html_dateMlist);

    $(document).ready(function(e) {
        $("[name='dateMword']").on('change', function() {
            $.ajax({
                synch: 'true',
                type: "POST",
                url: url_update_ref,
                data: {
                    'id': data['id'],
                    'dateMword': $("#id-update-dateM_from_form").val()
                },
                dataType: 'json',
                success: function(responseData) {
                    let html_table;
                    html_table = edit_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });
            return false;
        });
    }, false);
});

// Update dateY (Selected ref)
document.getElementById("id-update-selected-dateY").addEventListener("input", function() {
    var newdate = $('#id-update-selected-dateY').html();
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'dateY': newdate,
        },
        dataType: 'json',
        success: function (responseData) {
            let html_table;
            html_table = edit_table(responseData);
            $("#listRef_"+data['id']).html(html_table);
        }
    });

}, false);


// Update Folder (Selected ref)
$( "#id-update-selected-folder" ).one( "click", function() {
    let html_folderlist;

    html_folderlist = "<form action='' method='POST' id='id-selection-folder_form'>"
        + csrf_token_folder
        + "<select id='id-update-folder_from_form' name='folder' onchange='this.form.submit()'>"
        + "<option value='" + data['folder'] + "'>" + data['folder'] + "</option>";
    
    for(i = 0; i < folder_list.length; i++){
        if(!(folder_list[i] == data['folder'])){
            html_folderlist += "<option value='" + folder_list[i] + "'>" + folder_list[i] + "</option>"
        }
    };

    html_folderlist += "</select></form>"
    $("#id-update-selected-folder").html(html_folderlist);

    $(document).ready(function(e) {
        $("[name='folder']").on('change', function() {
            $.ajax({
                synch: 'true',
                type: "POST",
                url: url_update_ref,
                data: {
                    'id': data['id'],
                    'folder': $("#id-update-folder_from_form").val()
                },
                dataType: 'json',
                success: function(responseData) {
                    let html_table;
                    html_table = edit_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });
            return false;
        });
    }, false);
});


// Update type (Selected ref)
$( "#id-update-selected-type" ).one( "click", function() {
    let html_typelist;

    html_typelist = "<form action='' method='POST' id='id-selection-type_form'>"
        + csrf_token_folder
        + "<select id='id-update-type_from_form' name='type' onchange='this.form.submit()'>"
        + "<option value='" + data['foltypeder'] + "'>" + data['type'] + "</option>";
    
    for(i = 0; i < type_ref.length; i++){
        if(!(type_ref[i] == data['type'])){
            html_typelist += "<option value='" + type_ref[i] + "'>" + type_ref[i] + "</option>"
        }
    };

    html_typelist += "</select></form>"
    $("#id-update-selected-type").html(html_typelist);

    $(document).ready(function(e) {
        $("[name='type']").on('change', function() {
            $.ajax({
                synch: 'true',
                type: "POST",
                url: url_update_ref,
                data: {
                    'id': data['id'],
                    'type': $("#id-update-type_from_form").val()
                },
                dataType: 'json',
                success: function(responseData) {
                    let html_table;
                    html_table = edit_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });
            return false;
        });
    }, false);
});

// Delete ref (Selected ref)
document.getElementById("id-delete-selected-ref").addEventListener("click", function() {
    var delete_ref = true;
    $.ajax({
        synch: 'true',
        url: url_update_ref,
        type: 'POST',
        data: {
            'id': data['id'],
            'delete_ref': delete_ref,
        },
        dataType: 'json',
        success: function (responseData) {
            window.location.replace('/');
        }
    });
}, false);