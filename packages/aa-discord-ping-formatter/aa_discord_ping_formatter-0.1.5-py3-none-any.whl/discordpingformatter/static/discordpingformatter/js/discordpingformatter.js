jQuery(document).ready(function($) {
    /**
     * convert line breaks into <br>
     *
     * @param {string} string
     * @param {bool} isXhtml
     */
    var nl2br = (function(string, isXhtml) {
        var breakTag = (isXhtml || typeof isXhtml === 'undefined') ? '<br />' : '<br>';

        return (string + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
    });

    /**
     * closing the message
     *
     * @param {string} element
     * @returns {void}
     */
    var closeCopyMessageElement = (function(element) {
        /**
         * close after 10 seconds
         */
        $(element).fadeTo(10000, 500).slideUp(500, function() {
            $(this).slideUp(500, function() {
                $(this).remove();
            });
        });
    });

    /**
     * show message when copy action was successful
     *
     * @param {string} message
     * @param {string} element
     * @returns {undefined}
     */
    var showSuccess = (function(message, element) {
        $(element).html('<div class="alert alert-success alert-dismissable alert-copy-success"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message + '</div>');

        closeCopyMessageElement('.alert-copy-success');

        return;
    });

    /**
     * show message when copy action was not successful
     *
     * @param {string} message
     * @param {string} element
     * @returns {undefined}
     */
    var showError = (function(message, element) {
        $(element).html('<div class="alert alert-danger alert-dismissable alert-copy-error"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message + '</div>');

        closeCopyMessageElement('.alert-copy-error');

        return;
    });

    /**
     * sanitize input string
     *
     * @param {string} element
     * @returns {undefined}
     */
    var sanitizeInput = (function(input) {
        return input.replace(/<(|\/|[^>\/bi]|\/[^>bi]|[^\/>][^>]+|\/[^>][^>]+)>/g, '');
    });

    /**
     * send a message to a Discord webhook
     *
     * @param {string} discordWebhook
     * @param {string} discordPingText
     */
    var sendDiscordPing = (function(discordWebhook, discordPingText) {
        var request = new XMLHttpRequest();

        request.open("POST", discordWebhook);
        request.setRequestHeader('Content-type', 'application/json');

        var params = {
            username: "",
            avatar_url: "",
            content: discordPingText
        };

        request.send(JSON.stringify(params));
    });

    // generate the ping text
    $('button#createPingText').on('click', function() {
        var pingTarget = sanitizeInput($('select#pingTarget option:selected').val());
        var fleetType = sanitizeInput($('select#fleetType option:selected').val());
        var fcName = sanitizeInput($('input#fcName').val());
        var fleetName = sanitizeInput($('input#fleetName').val());
        var formupLocation = sanitizeInput($('input#formupLocation').val());
        var formupTime = sanitizeInput($('input#formupTime').val());
        var fleetComms = sanitizeInput($('input#fleetComms').val());
        var fleetDoctrine = sanitizeInput($('input#fleetDoctrine').val());
        var fleetSrp = sanitizeInput($('select#fleetSrp option:selected').val());
        var additionalInformation = sanitizeInput($('textarea#additionalInformation').val());

        // ping webhooks, if configured
        var discordWebhook = false;

        if($('select#pingChannel').length) {
            discordWebhook = sanitizeInput($('select#pingChannel option:selected').val());
        }

        $('.aa-discord-ping-formatter-ping').show();

        var discordPingText = '';
        discordPingText += pingTarget + ' :: ';

        discordPingText += '**';

        // check if it's a preping or not
        if($('input#prePing').is(':checked')) {
            discordPingText += '### PRE PING ###';

            if(fleetType !== '') {
                discordPingText += ' / ' + fleetType + ' Fleet'
            }
        } else {
            if(fleetType !== '') {
                discordPingText += fleetType + ' ';
            }

            discordPingText += 'Fleet is up';
        }

        discordPingText += '**' + "\n";

        // check if FC name is available
        if(fcName !== '') {
            discordPingText += "\n" + '**FC:** ' + fcName;
        }

        // check if fleet name is available
        if(fleetName !== '') {
            discordPingText += "\n" + '**Fleet Name:** ' + fleetName;
        }

        // check if formup location is available
        if(formupLocation !== '') {
            discordPingText += "\n" + '**Formup Location:** ' + formupLocation;
        }

        // check if formup time is available
        if(formupTime !== '') {
            discordPingText += "\n" + '**Formup Time:** ' + formupTime ;
        }

        // check if fleet comms is available
        if(fleetComms !== '') {
            discordPingText += "\n" + '**Comms:** ' + fleetComms;
        }

        // check if doctrine is available
        if(fleetDoctrine !== '') {
            discordPingText += "\n" + '**Ships / Doctrine:** ' + fleetDoctrine;
        }

        // check if srp is available
        if(fleetSrp !== '') {
            discordPingText += "\n" + '**SRP:** ' + fleetSrp;
        }

        // check if additional information is available
        if(additionalInformation !== '') {
            discordPingText += "\n\n" + '**Additional Information**:' + "\n" + additionalInformation;
        }

        $('.aa-discord-ping-formatter-ping-text').html('<p>' + nl2br(discordPingText) + '</p>');

        // ping it directly if a webhook is selected
        if(discordWebhook !== false && discordWebhook !== '') {
            sendDiscordPing(discordWebhook, discordPingText);

            // tell the FC that it's already pinged
            showSuccess('Success, your ping has been sent to your Discord.', '.aa-discord-ping-formatter-ping-copyresult');
        }
    });

    /**
     * Copy permalink to clipboard
     */
    $('button#copyDiscordPing').on('click', function() {
        /**
         * copy permalink to clipboard
         *
         * @type Clipboard
         */
        var clipboardDiscordPingData = new Clipboard('button#copyDiscordPing');

        /**
         * copy success
         *
         * @param {type} e
         */
        clipboardDiscordPingData.on('success', function(e) {
            showSuccess('Success, Ping copied to clipboard. Now be a good FC and throw it in your Discord so you actually get some people in fleet.', '.aa-discord-ping-formatter-ping-copyresult');

            e.clearSelection();
            clipboardDiscordPingData.destroy();
        });

        /**
         * copy error
         */
        clipboardDiscordPingData.on('error', function() {
            showError('Error, Ping not copied to clipboard.', '.aa-discord-ping-formatter-ping-copyresult');

            clipboardDiscordPingData.destroy();
        });
    });
});
