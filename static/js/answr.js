// The namespace of answr.js
var ANSWR = {
    'fbs_click' : function(idd) {
        u = 'http://www.answr.it/q?id='+idd;
        t = document.title;
        fb_url = 'http://www.facebook.com/sharer.php?u='+encodeURIComponent(u)+'&t='+encodeURIComponent(t);
        window.open(fb_url,'sharer','toolbar=0,status=0,width=626,height=436');
        return false;
    },

    'answrd' : false,

    'strings' : {
        'en' : {
            'must_ask' : 'You must ask something!',
            "type_your_question" : "Type your question"
        },
        'it' : {
            "must_ask" : "Devi chiedere qualcosa!",
            "type_your_question" : "Scrivi la tua domanda"
        }
    },

    'answrit' : function() {
        if(!ANSWR.answrd){
            if($("input#input_cerca").val() == ANSWR.strings[lang]['type_your_question'] || $("input#input_cerca").val() == ""){
                alert(ANSWR.strings[lang]['must_ask']);
            }
            else{
                $("#risposta").hide();
                $("#loading").show();
                $.get("/answr", {'lang' : lang, 'question' :  $("input#input_cerca").val()}, 
                    function(data){
                        data = JSON.parse(data);

                        $("#risposta > #text").text(data["text"]);
                        $("#loading").fadeOut("slow", function(){
                            $("#risposta").fadeIn("slow",function(){
                                
                                $("input#input_cerca").attr("disabled", true);
                                $("input#input_cerca").css("width", "750px");
                                $("#img_cerca").fadeOut();
                                $("#risposta").animate({ 
                                        fontSize: 40
                                    }, 1500 ,function() {
                                        $("#reload").fadeIn('slow');
                                        ANSWR.blink();
                                    }
                                );
                            });
                        });
                    }
                );
            }
            ANSWR.answrd = true;
        }
        return false;
    }, 

    'blink' : function() {
        $('#reload_text').fadeIn('slow',function(){
            $('#reload_text').fadeOut('slow',function(){
                $('#previous').fadeOut('slow');
                ANSWR.blink();
            })
        });
    }
};

