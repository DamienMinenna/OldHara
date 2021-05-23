
// Display modal if needed
if (isModalAF) {
    $('#Modaladdfolder').modal('show');
}

// Display modal if needed
if (isModalD) {
    $('#ModaladdDOI').modal('show');
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
    + "<td id='appadd'>" + getAuthors_table(responseData) + "</td>"
    + "<td id='appadd'>" + responseData['message']['title'] + "</td>"
    + "<td id='appadd'>" + getDate_table(responseData) + "</td>"
    + "<td id='appadd'>" + getJournal(responseData) + "</td>";
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

        $('#detail_type').html(data['message']['type']);
        $('#detail_title').html(data['message']['title']);
        $('#detail_authors').html(getAuthors(data));
        $('#detail_journal').html(getJournal(data));
        $('#detail_date').html(getDate(data));
        $('#detail_volume').html("<div contenteditable='true' id='editVolume' style='display: inline-block;'>" + data['message']['volume'] + "</div>");
        $('#detail_issue').html(data['message']['issue']);
        $('#detail_page').html(data['message']['page']);
        $('#detail_artnumber').html(data['message']['article-number']);

        $('#detail_doi').html("<a target='_blank' href='https://doi.org/" + data['message']['DOI'] + "'>" + data['message']['DOI'] + "</a>");
        $('#detail_badgedimension').html("<span class='__dimensions_badge_embed__' data-doi=" + data['message']['DOI'] + " data-style='small_rectangle'></span>" + "<div data-badge-popover='left' data-link-target='_blank' data-hide-no-mentions='true' data-doi=" + data['message']['DOI'] + " class='altmetric-embed'></div>");
        $('#detail_folder').html("<div id='editFolder' style='display: inline-block;'>" + data['OldHara']['folder'] + "</div>");

        window.__dimensions_embed.addBadges()
        _altmetric_embed_init();

        $("#listRef_"+data['OldHara']['id']).addClass("table-selected");

        // Edit volume
        document.getElementById("editVolume").addEventListener("input", function() {
            var volume = $('#editVolume').html();
            $.ajax({
                synch: 'true',
                url: urlmodify_biblio,
                type: 'POST',
                data: {
                    'id': data['OldHara']['id'],
                    'volume': volume,
                },
                dataType: 'json',
                success: function (responseData) {
                    let html_table;
                    html_table = change_table(responseData);
                    $("#listRef_"+data['OldHara']['id']).html(html_table);
                }
            });

        }, false);

        // Edit folder
        $( "#editFolder" ).one( "click", function() {
            let html_folderlist;

            html_folderlist = "<form action='' method='POST' id='formSelectFolder'>"
                + csrf_token_folder
                + "<select id='selectFolder' name='folder' onchange='this.form.submit()'>"
                + "<option value='" + data['OldHara']['folder'] + "'>" + data['OldHara']['folder'] + "</option>";
            
            for(i = 0; i < folder_list.length; i++){
                if(!(folder_list[i] == data['OldHara']['folder'])){
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
                            'id': data['OldHara']['id'],
                            'folder': $("#selectFolder").val()
                        },
                        dataType: 'json',
                        success: function(responseData) {
                            let html_table;
                            html_table = change_table(responseData);
                            $("#listRef_"+data['OldHara']['id']).html(html_table);
                        }
                    });
                    return false;
                });
            }, false);
        });

    } catch (error) {
        console.error('no json');
        $('#details').html('Select an item');
        window.__dimensions_embed.addBadges()
        _altmetric_embed_init();
    }
});