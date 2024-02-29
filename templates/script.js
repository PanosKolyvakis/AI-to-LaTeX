
$(document).ready(function() {
    // Function to execute search
    function executeSearch() {
        var query = $('#searchQuery').val();
        var templateUsed = $('#templateUsed').val();
        var name = $('#inputName').val();
        var date = $('#inputDate').val();
        var title = $('#inputTitle').val();
        $('#aiThinkingAnimation').show();

        $.ajax({
            type: "POST",
            url: "/search-to-blog",
            contentType: "application/json",
            data: JSON.stringify({ query, template: templateUsed, name, date, title }),
            success: function(response) {
                $('#aiThinkingAnimation').hide();
                checkPdfReady('response.pdf', 12);
            },
            error: function(xhr, status, error) {
                $('#aiThinkingAnimation').hide();
                console.error("Error: ", status, " ", error);
            }
        });
    }

    $('#searchButton').click(function() {
        executeSearch();
    });

    $('#searchForm input').on('keypress', function(e) {
        if (e.which == 13) { 
            e.preventDefault();
            executeSearch();
        }
    });

    $('#refineButton').click(function() {
        $('#largeTextbox, #submitRefinement').toggle();
    });

    $('#additionalDetailsButton').click(function() {
        $('#additionalDetailsForm').toggle();
    });

    $('#submitDetails').click(function() {
        var name = $('#inputName').val();
        var date = $('#inputDate').val();
        var title = $('#inputTitle').val();
        // Perform any action needed with the details, then hide the form
        console.log("Details submitted:", { name, date, title });
        $('#additionalDetailsForm').hide();
    });

    $('#submitRefinement').click(function() {
        var refinementDetails = $('#largeTextbox').val();
        $('#aiThinkingAnimation').show();
        $.ajax({
            type: "POST",
            url: "/submit-refinement",
            contentType: "application/json",
            data: JSON.stringify({ refinement_details: refinementDetails }),
            success: function(response) {
                $('#aiThinkingAnimation').hide();
                console.log("Refinement submitted successfully:", response);
                checkPdfReady('response.pdf', 12);
            },
            error: function(xhr, status, error) {
                $('#aiThinkingAnimation').hide();
                console.error("Error submitting refinement:", status, " ", error);
            }
        });
        $('#largeTextbox, #submitRefinement').hide();
    });

    $('#editTexButton').click(function() {
        $('#texEditor').toggle();
        $('#submitTexEditsButton').toggle($('#texEditor').is(':visible'));

        if ($('#texEditor').is(':visible')) {
            $.get('/static/docs/response.tex', function(data) {
                $('#texEditor').val(data);
            }).fail(function() {
                $('#texEditor').val('Failed to load .tex content.');
            });
        }
    });

    $('#submitTexEditsButton').click(function() {
        var editedTexContent = $('#texEditor').val();
        $('#aiThinkingAnimation').show();
        $.ajax({
            type: "POST",
            url: "/submit-edited-tex",
            contentType: "application/json",
            data: JSON.stringify({ texContent: editedTexContent }),
            success: function(response) {
                setTimeout(function() {
                    $('#aiThinkingAnimation').hide();
                    var timestamp = new Date().getTime();
                    $('iframe').attr('src', '/static/docs/response.pdf?' + timestamp);
                }, 1000);
            },
            error: function(xhr, status, error) {
                $('#aiThinkingAnimation').hide();
                // Update the .right or #pdfViewer div to show a custom message
                $('.right').html('<div style="color: white; text-align: center; padding-top: 20%; font-size: 20px;">Document does not compile to .pdf</div>');
                // Hide the .tex editor and the submit button
                $('#texEditor, #submitTexEditsButton').hide();
            }
        });
        $('#texEditor, #submitTexEditsButton').hide();
    });

    function checkPdfReady(filename, attemptsLeft) {
        if (attemptsLeft <= 0) {
            $('#aiThinkingAnimation').hide();
            $('#pdfViewer').html('<div style="color: white; text-align: center;">Document does not compile to .pdf</div>');
            return;
        }

        $.ajax({
            type: "GET",
            url: "/pdf-ready/" + filename,
            success: function(response) {
                if (response.ready) {
                    $('#aiThinkingAnimation').hide();
                    var timestamp = new Date().getTime();
                    $('iframe').attr('src', '/static/docs/' + filename + '?' + timestamp);
                } else {
                    setTimeout(() => checkPdfReady(filename, attemptsLeft - 1), 5000);
                }
            },
            error: function() {
                $('#aiThinkingAnimation').hide();
                $('#pdfViewer').html('<div style="color: white; text-align: center;">Error checking PDF readiness.</div>');
            }
        });
    }
});
