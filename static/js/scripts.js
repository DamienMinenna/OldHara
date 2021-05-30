
// Display modal if needed
if (isModalAF) {
    $('#Modaladdfolder').modal('show');
}

// Hide the menu
function openMenu() {
    if (document.getElementById("main_sidebar").style.display === "none") {
        document.getElementById("main_sidebar").style.display = "block";
        document.getElementById("main_container").classList.remove('col-9')
        document.getElementById("main_container").classList.add('col-7')
    } else {
        document.getElementById("main_sidebar").style.display = "none";
        document.getElementById("main_container").classList.remove('col-7')
        document.getElementById("main_container").classList.add('col-9')
    } 
}


// retrive database
function getAuthors(data) {
    let authors;
    if (typeof data['message']['author'] != "undefined") {
        for(var key in data['message']['author']){
            authors +=  data['message']['author'][key]['given'] + ' ' + data['message']['author'][key]['family'] + ', '
        }
        return authors.slice(0, -2).substring(9);
    }
    return "undefined"
}

function getAuthors_table(data) {
    let authors;
    if (typeof data['message']['author'] != "undefined") {
        for(var key in data['message']['author']){
            authors +=  data['message']['author'][key]['family'] + ', ' + data['message']['author'][key]['given'] + '; '
        }
        return authors.slice(0, -2).substring(9);
    }
    return ""
}

function getJournal(data) {
    if (typeof data['message']['container-title'] != "undefined") {
        return data['message']['container-title'][0];
    }
    return "undefined";
}

function getDate(data) {
    if (typeof data['message']['issued'] != "undefined") {
        if (typeof data['message']['issued']['date-parts'] != "undefined") {
            return data['message']['issued']['date-parts'];
        }
    }
    return "undefined";
}

function getDate_table(data) {
    if (typeof data['message']['issued'] != "undefined") {
        if (typeof data['message']['issued']['date-parts'] != "undefined") {
            return data['message']['issued']['date-parts'][0][0];
        }
    }
    return "";
}

function change_table(responseData) {
    let html
    html = "<td id='appadd'>" + JSON.stringify(responseData) + "</td>"
    + "<td id='appadd'></td>"
    + "<td id='appadd'>" + responseData['listauthor'] + "</td>"
    + "<td id='appadd'>" + responseData['title'] + "</td>"
    + "<td id='appadd'>" + responseData['dateY'] + "</td>"
    + "<td id='appadd'>" + responseData['journal'] + "</td>";
    return html
}

$("#tableList").on('click', 'tr', function()  {

    

    // Remove class table-selected 
    var table = document.getElementById("tableList");
    for (var i = 1, row; row = table.rows[i]; i++) {
        var idTable = table.rows[i].id
        if($("#" + idTable).hasClass("table-selected")){
            $("#" + idTable).removeClass("table-selected")
        }
    }

    var data = $(this).find('td:first-child').text();
    try {
        
        data = JSON.parse(data)

        $('#detail_folder').html("<div id='editFolder' class='detail-editable'>" + data['folder'] + "</div>");
        $('#detail_type').html(data['type']);
        $('#detail_title').html("<div contenteditable='true' id='editTitle' class='detail-editable'>" + data['title'] + "</div>");
        $('#detail_authors').html(data['listauthor']);
        $('#detail_journal').html(data['journal']);
        $('#detail_date').html(data['dateY']);
        $('#detail_volume').html("<div contenteditable='true' id='editVolume' class='detail-editable'>" + data['volume'] + "</div>");
        $('#detail_issue').html("<div contenteditable='true' id='editIssue' class='detail-editable'>" + data['issue'] + "</div>");
        $('#detail_page').html("<div contenteditable='true' id='editPage' class='detail-editable'>" + data['page'] + "</div>");
        $('#detail_artnumber').html("<div contenteditable='true' id='editArtNumb' class='detail-editable'>" + data['articlenumber'] + "</div>");

        $('#detail_doi').html("<a target='_blank' href='https://doi.org/" + data['DOI'] + "'>" + data['DOI'] + "</a>");
        $('#detail_badgedimension').html("<span class='__dimensions_badge_embed__' data-doi=" + data['DOI'] + " data-style='small_rectangle'></span>" + "<div data-badge-popover='left' data-link-target='_blank' data-hide-no-mentions='true' data-doi=" + data['DOI'] + " class='altmetric-embed'></div>");
        
        window.__dimensions_embed.addBadges()
        _altmetric_embed_init();

            
        $("#listRef_"+data['id']).addClass("table-selected");

        // Edit Title
        document.getElementById("editTitle").addEventListener("input", function() {
            var edtitle = $('#editTitle').html();
            $.ajax({
                synch: 'true',
                url: urlmodify_biblio,
                type: 'POST',
                data: {
                    'id': data['id'],
                    'title': edtitle,
                },
                dataType: 'json',
                success: function (responseData) {
                    let html_table;
                    html_table = change_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });

        }, false);

        // Edit volume
        document.getElementById("editVolume").addEventListener("input", function() {
            var edvolume = $('#editVolume').html();
            $.ajax({
                synch: 'true',
                url: urlmodify_biblio,
                type: 'POST',
                data: {
                    'id': data['id'],
                    'volume': edvolume,
                },
                dataType: 'json',
                success: function (responseData) {
                    let html_table;
                    html_table = change_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });

        }, false);

        // Edit Issue
        document.getElementById("editIssue").addEventListener("input", function() {
            var edissue = $('#editIssue').html();
            $.ajax({
                synch: 'true',
                url: urlmodify_biblio,
                type: 'POST',
                data: {
                    'id': data['id'],
                    'issue': edissue,
                },
                dataType: 'json',
                success: function (responseData) {
                    let html_table;
                    html_table = change_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });

        }, false);

        // Edit Page
        document.getElementById("editPage").addEventListener("input", function() {
            var edpage = $('#editPage').html();
            $.ajax({
                synch: 'true',
                url: urlmodify_biblio,
                type: 'POST',
                data: {
                    'id': data['id'],
                    'page': edpage,
                },
                dataType: 'json',
                success: function (responseData) {
                    let html_table;
                    html_table = change_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });

        }, false);

        // Edit Article number
        document.getElementById("editArtNumb").addEventListener("input", function() {
            var edArtNumb = $('#editArtNumb').html();
            $.ajax({
                synch: 'true',
                url: urlmodify_biblio,
                type: 'POST',
                data: {
                    'id': data['id'],
                    'ArtNumb': edArtNumb,
                },
                dataType: 'json',
                success: function (responseData) {
                    let html_table;
                    html_table = change_table(responseData);
                    $("#listRef_"+data['id']).html(html_table);
                }
            });

        }, false);

        // Edit folder
        $( "#editFolder" ).one( "click", function() {
            let html_folderlist;

            html_folderlist = "<form action='' method='POST' id='formSelectFolder'>"
                + csrf_token_folder
                + "<select id='selectFolder' name='folder' onchange='this.form.submit()'>"
                + "<option value='" + data['folder'] + "'>" + data['folder'] + "</option>";
            
            for(i = 0; i < folder_list.length; i++){
                if(!(folder_list[i] == data['folder'])){
                    html_folderlist += "<option value='" + folder_list[i] + "'>" + folder_list[i] + "</option>"
                }
            };

            html_folderlist += "</select></form>"
            $("#editFolder").html(html_folderlist);

            $(document).ready(function(e) {
                $("[name='folder']").on('change', function() {
                    $.ajax({
                        synch: 'true',
                        type: "POST",
                        url: urlmodify_biblio,
                        data: {
                            'id': data['id'],
                            'folder': $("#selectFolder").val()
                        },
                        dataType: 'json',
                        success: function(responseData) {
                            let html_table;
                            html_table = change_table(responseData);
                            $("#listRef_"+data['id']).html(html_table);
                        }
                    });
                    return false;
                });
            }, false);
        });

    } catch (error) {
        console.error('no json');
        
        window.__dimensions_embed.addBadges()
        _altmetric_embed_init();
    }
});
