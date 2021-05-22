
// Display modal if needed
if (isModalAF) {
    $('#Modaladdfolder').modal('show');
}

// Display modal if needed
if (isModalD) {
    $('#ModaladdDOI').modal('show');
}

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
    + "<td id='appadd'>" + getJournal(responseData) + "</td>"
    + "<td id='appadd'></td>";
    return html
}

$("#tableList").on('click', 'tr', function()  {
    var data = $(this).find('td:first-child').text();
    try {
        data = JSON.parse(data)

        let html;
        html = " <li class='list-group-item'>id: " + data['OldHara']['id'] + "</li> "
            + " <li class='list-group-item'>Type: " + data['message']['type'] + "</li> "
            + "<li class='list-group-item'>Title: <b>" + data['message']['title'] + "</b></li>"
            + "<li class='list-group-item'>Authors: " + getAuthors(data) + "</li> "
            + "<li class='list-group-item'>Journal: " + getJournal(data) + "</li> "
            + "<li class='list-group-item'>Date: " + getDate(data) + "</li> "
            + "<li class='list-group-item'>Volume: <div contenteditable='true' id='editVolume'>" + data['message']['volume'] + "</div> </li> "
            + "<li class='list-group-item'>Issue: " + data['message']['issue'] + "</li> "
            + "<li class='list-group-item'>Pages: " + data['message']['page'] + "</li> "
            + "<li class='list-group-item'>Article number: " + data['message']['article-number'] + "</li> "
            + "<li class='list-group-item'>Pages: " + data['message']['page'] + "</li> "
            + "<li class='list-group-item'>DOI: <a target='_blank' href='https://doi.org/" + data['message']['DOI'] + "'>" + data['message']['DOI'] + "</a></li> "
            + "<li class='list-group-item'> <span class='__dimensions_badge_embed__' data-doi=" + data['message']['DOI'] + " data-style='small_rectangle'></span>"
            + "<div data-badge-popover='left' data-link-target='_blank' data-hide-no-mentions='true' data-doi=" + data['message']['DOI'] + " class='altmetric-embed'></div></li> "
            + "<li class='list-group-item'>Folder: <div id='editFolder'>" + data['OldHara']['folder'] + "</div> </li> "
            + " ";

        $('#details').html(html);
        window.__dimensions_embed.addBadges()
        _altmetric_embed_init();

        document.getElementById("editVolume").addEventListener("input", function() {
            var volume = $('#editVolume').html();
            $.ajax({
                synch: 'true',
                url: urlVolume,
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
                        url: urlFolder,
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
            });
        });

    } catch (error) {
        console.error('no json');
        $('#details').html('Select an item');
        window.__dimensions_embed.addBadges()
        _altmetric_embed_init();
    }
});