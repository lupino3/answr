# -*- encoding: utf8 -*-
from models import Answr
import logging
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class PopulatePage(webapp.RequestHandler):
    def get(self):
        self.log("Populating the DB...")
        answrs = {"en" : 
            ["No", "Maybe", "Better luck next time", "You have to believe it", "Of course", "You will improve your situation", "Think slower", "Absolutely", "It is better to wait", "Keep it for yourself", "No space for doubts", "Be patient", "Be careful and keep watching", "You will be glad of doing it", "Keep it simple", "Keep improving yourself", "Don't ask anything more", "The best solution may not be the most obvious", "It is out of your control", "Watch your step", "Talk about it with a friend before doing anything", "Don't be shy", "It's a good moment for your projects", "Things will change around you", "It's important", "Don't wait", "You will not forget it", "Try to look around", "Take it easy", "You have to risk something", "You will need to know more about it", "You are not objective", "Now you can", "It will make things more interesting", "It is not as sure as you might think", "It's not important", "Tell someone how important they are", "Open your mind", "Open your eyes", "Don't talk too much", "It's a good moment to start new projects", "You will get the desired result", "Somebody will help you", "Do it now", "Keep going", "Stop now, you can still limit damage", "Maybe it's easier than you thought", "Take your time", "Enjoy yourself", "Listen more carefully, and you will understand", "Only you know the answer", "Keep it simple", "You don't really care", "Look around", "Don't waste your time", "It could be awesome", "It will be awesome", "It is not so important", "It is wrong", "Only you know what's really important", "Know yourself", "Try to relax", "Go out", "The answer is simpler than you might think", "Think about your lifestyle", "Your friends make you rich", "Believe in friendship", "Serenity is precious", "Find a solution as soon as possible", "It's not advisable", "It will cost you some extra effort", "You know by yourself", "Sometimes", "Don't waste your time", "You're too involved to understand your situation", "It will forever stay in your heart", "It will forever stay in your mind", "It's important", "You'll think about it later", "Things will be better"], 
            
            "it" : 
            [ "No", "Forse", "Sarai più fortunato", "Devi crederci", "Certamente", "Migliorerai la tua situazione", "Rifletti con attenzione", "Assolutamente", "È meglio aspettare", "Tienilo per te stesso", "Nessuno spazio per i dubbi", "Sii paziente", "Stai attento e continua ad osservare", "Ne sarai fiero", "Sii semplice", "Continua a migliorarti", "Non chiedere altro", "La soluzione migliore potrebbe non essere la più ovvia", "È fuori dal tuo controllo", "Occhio a dove metti i piedi", "Parlane con un amico prima di fare qualsiasi cosa", "Non essere timido", "È un buon momento per i tuoi progetti", "Le cose cambieranno attorno a te", "È importante", "Non aspettare", "Non lo dimenticherai", "Guardati attorno", "Devi rischiare qualcosa", "Avrai bisogno di saperne di più", "Non sei oggettivo", "Ora puoi", "Renderà tutto molto più interessante", "Non esserne certo", "Non è importante", "Di' a qualcuno quant'è importante per te", "Apri la tua mente", "Apri i tuoi occhi", "Non parlare troppo", "È un buon momento per avviare nuovi progetti", "Otterrai i risultati desiderati", "Qualcuno ti aiuterà", "Fallo ora", "Continua così", "Fermati, puoi ancora limitare i danni", "Forse è più facile di quanto pensi", "Prenditi il tuo tempo", "Divertiti", "Ascolta con più attenzione, e capirai", "Solo tu conosci la risposta", "Non ti interessa davvero", "Guardati attorno", "Non sprecare il tuo tempo", "Potrebbe essere grandioso", "Non è così importante", "È sbagliato", "Solo tu sai ciò che è davvero importante", "Conosci te stesso", "Prova a rilassarti", "Va' fuori", "Sarà grandioso", "La risposta è più semplice di quanto credi", "Pensa al tuo stile di vita", "I tuoi amici ti rendono ricco", "Credi nell'amicizia", "La serenità è preziosa", "Trova una soluzione prima possibile", "Non è consigliabile", "Dovrai lavorare molto", "Lo sai tu stesso", "A volte", "Non perdere il tuo tempo", "Sei troppo coinvolto per capire la tua situazione", "Resterà per sempre nel tuo cuore", "Resterà per sempre nella tua mente", "È importante", "Ci penserai successivamente", "Le cose miglioreranno"]
        }

        for lang, lang_answrs in answrs.iteritems():
            for answr_text in lang_answrs:
                self.log('Adding answr "%s"' % answr_text)
                Answr.add_answr(answr_text, lang)

        Answr.add_answr("Something strange is going on..", "en", 1.0)
        Answr.add_answr("Sta accadendo qualcosa di strano..", "it", 1.0)
        self.log('Done')

    def log(self, msg):
        self.response.out.write(msg)
        logging.info(msg)


application = webapp.WSGIApplication([('/populate', PopulatePage)])

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
