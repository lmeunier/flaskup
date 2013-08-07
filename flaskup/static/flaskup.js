var ErrorMessage = Backbone.Model.extend({
    initialize: function() {
        this.set({message: undefined});
    }
});


var ErrorMessageView = Backbone.View.extend({
    el: $('#error-message'),
    template: _.template($('#error-message-template').html()),

    initialize: function() {
        this.message = new ErrorMessage;
        this.listenTo(this.message, 'change', this.render);
    },

    render: function() {
        this.$el.html(this.template({message: this.message.get('message')}));
        return this;
    },
});


var MyfileModel = Backbone.Model.extend({
    initialize: function() {
        this.s(undefined);
    },
    s: function(file) {
        // shortcut function to set the file
        this.set({'file': file});
    },
    g: function() {
        // shortcut function to get the file
        return this.get('file');
    },
});


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
        // create our unique MyfileModel
        this.myfile = new MyfileModel;
        // ... and listen to changes (to update UI)
        this.listenTo(this.myfile, 'change', this.render);

        // initialize UI
        this.render();
    },

    render: function() {
        this.$el.html(this.template({myfile: this.myfile.g()}));
        return this;
    },

    file_select: function(files) {
        this.myfile.s(files[0]);
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
        this.myfile.s(undefined);
    },
});


var UploadProgressModel = Backbone.Model.extend({
    initialize: function() {
        this.reset();
    },

    reset: function() {
        this.set({
            last_datetime: new Date(),
            last_size: 0,
            speed: 0,
            total: 0,
        });
    },

    compute: function(evt) {
        if(!evt.lengthComputable) {
            return;
        }

        var speed = this.get('speed');
        var current_datetime = new Date();
        var diff_datetime = (current_datetime - this.get('last_datetime')) / 1000;
        if(diff_datetime > 1) {
            // compute speed every second
            var diff_size = evt.loaded - this.get('last_size');
            var speed = diff_size / diff_datetime;
        }

        this.set({
            last_datetime: current_datetime,
            last_size: evt.loaded,
            speed: speed,
            total: evt.total,
        });
    },

    percent: function() {
        return this.get('last_size') / this.get('total') * 100;
    }
});


var UploadProgressView = Backbone.View.extend({
    el: $('#js-progress'),
    template: _.template($('#progress-template').html()),

    initialize: function() {
        this.progress = new UploadProgressModel;
        this.listenTo(this.progress, 'change', this.render);
        this.render();
    },

    render: function() {
        this.$el.html(this.template({
            progress: this.progress,
        }));
        return this;
    },
});


var FlaskupView = Backbone.View.extend({
    el: $('#flaskup-app'),

    events: {
        "click #btn-submit": "start_upload",
        "click #btn-cancel": "stop_upload",
        "hidden #upload_modal": "stop_upload",
    },

    initialize: function() {
        // hide browser warning
        $('#crappy-browser-warning').hide();

        // create internal views
        this.errormessageview = new ErrorMessageView
        this.myfileview = new MyfileView;
        this.progressview = new UploadProgressView;
    },

    start_upload: function() {
        // prepare form data
        var form = document.getElementById('form-upload');
        var fd = new FormData(form);
        fd.append('myfile', this.myfileview.myfile.g());

        // create XHR
        this.xhr = new XMLHttpRequest();
        this.xhr.open('POST', '/upload');  // TODO
        this.xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        // create references to various Backbone.Model instances
        // they will be used in callbacks
        var progress = this.progressview.progress;
        var errormessage = this.errormessageview.message;

        // hide previous error messages
        errormessage.set({message: undefined});

        // Event: update the progress bar
        this.xhr.upload.addEventListener('progress', function(evt) {
            // wait the first 'progress' event to display the modal
            $('#upload_modal').modal();

            progress.compute(evt);
        }, false);

        // Event: upload is complete
        this.xhr.addEventListener('load', function(evt) {
            progress.compute(evt);

            // parse response from the server
            var response;
            try {
                response = JSON.parse(evt.target.responseText);
            } catch(e) {
                response = {
                    message: 'There was an error attempting to upload the file.', // TODO
                };
            }

            // something goes wrong, display the error message
            if(evt.target.status != 200) {
                $('#upload_modal').modal('hide');
                errormessage.set({message: response.message});
                return;
            }

            // follow the link returned by the server
            document.location.href = response.url;
        }, false);

        // Event: error when uploading
        this.xhr.addEventListener('error', function(evt) {
            progress.reset();
            $('#upload_modal').modal('hide');

            errormessage.set({message: 'There was an error attempting to upload the file.'}); // TODO
        }, false);

        // Event: upload canceled
        this.xhr.addEventListener('abort', function(evt) {
            progress.reset();
            $('#upload_modal').modal('hide');
        }, false);

        // and finally post XHR
        this.xhr.send(fd);

        return false;
    },

    stop_upload: function(evt) {
        this.xhr.abort();
    },
});
