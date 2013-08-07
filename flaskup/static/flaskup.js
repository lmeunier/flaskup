var MyfileView = Backbone.View.extend({
    el: $('#myfile-view'),
    template: _.template($('#myfile-template').html()),
    events: {
        "change #myfile": "event_select",
        "drop #myfile-drop": "event_drop",
        "dragover #myfile-drop": "event_dragover",
        "dragleave #myfile-drop": "event_dragleave",
        "click #myfile-drop": "event_clickdrop",
        "click #myfile-trash": "event_trash",
    },
    initialize: function() {
        this.render();
    },
    render: function() {
        this.$el.html(this.template({myfile: this.myfile}));
        return this;
    },
    file_select: function(files) {
        this.myfile = files[0];
        this.render();
    },
    event_select: function(evt) {
        this.file_select(evt.target.files);
    },
    event_drop: function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        this.file_select(evt.originalEvent.dataTransfer.files);
    },
    event_dragover: function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        evt.originalEvent.dataTransfer.dropEffect = 'copy';
        $('#myfile-drop').addClass('dragover');
    },
    event_dragleave: function(evt) {
        $('#myfile-drop').removeClass('dragover');
    },
    event_clickdrop: function(evt) {
        // simulate a click on an input[type=file] html element
        // to open the file select window
        $('#myfile').trigger('click');
    },
    event_trash: function(evt) {
        this.myfile = null;
        this.render();
    },
});

var FlaskupView = Backbone.View.extend({
    el: $('#flaskup-app'),
    initialize: function() {
        this.myfileview = new MyfileView();
    },
});
