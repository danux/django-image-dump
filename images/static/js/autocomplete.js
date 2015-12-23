/**
 * Adds autocomplete to the search box. Customised to show a thumbnail of the image.
 */
$(function(){
    var images = new Bloodhound({
        datumTokenizer: function(datum) { return Bloodhound.tokenizers.obj.whitespace(datum.value); },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: '/autocomplete/?q=%QUERY',
            wildcard: '%QUERY',
            filter: function(image_results) {
                return $.map(image_results.results, function(image) {
                    return {
                        title: image.title,
                        thumbnail: image.thumbnail,
                        url: image.url
                    }
                });
            }
        }
    });

    $('.typeahead').typeahead(null, {
        name: 'image-autocomplete',
        source: images,
        display: 'title',
        templates: {
            empty: [
                '<div class="empty-message">',
                'Sorry, no images found',
                '</div>'
            ].join('\n'),
            suggestion: Handlebars.compile('<div><img src="{{thumbnail}}"> <strong>{{title}}</strong></div>')
        }
    })
    .bind('typeahead:selected', function (obj, datum) {
        window.location.href = datum.url;
    });
});
