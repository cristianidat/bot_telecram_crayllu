from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import json
import yaml

updater=Updater(token='5757905250:AAHSLhkjSbahtCKkyiIY4lfxbYDBJYBfcw4', use_context=True)
dispatcher = updater.dispatcher

with open("info.json") as data:
        datos=json.load(data)

with open("imagenes.json") as imagen:
        img=json.load(imagen)

indice=list(datos.keys())
indice_mochilas=list(datos["mochilas"].keys())
indice_carteras=list(datos["carteras"].keys())
indice_juguetes=list(datos["Juguetes"].keys())

def start(update: Updater,context: CallbackContext): #Comando para dar inicio a las instruciones. 
    #context.bot.send_message(chat_id=update.effective_chat.id, text=yaml.dump(datos, sort_keys=False, default_flow_style=False))
        keyboard = [
        [
            InlineKeyboardButton("Mochilas", callback_data=yaml.dump(indice_mochilas, sort_keys=False, default_flow_style=False)),
            InlineKeyboardButton("Carteras", callback_data=yaml.dump(indice_carteras, sort_keys=False, default_flow_style=False)),
        ],
        [InlineKeyboardButton("Jueguetes", callback_data=yaml.dump(indice_juguetes, sort_keys=False, default_flow_style=False))],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Seleccione una de la categorias para ver la lista de Productos: ', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Escriba el nombre del producto que dese ver mas detalles: \n {query.data}")

def echo(update: Update, context: CallbackContext):
    #context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
        #with open("info.json") as data:
         #        datos=json.load(data)
        #indice=list(datos.keys())
        
        messegae_text=update.message.text
        url=img[messegae_text]
        for i in datos:
                for a in datos[i]:
                        if messegae_text==a:
                                cadena=datos[i][a]
                                context.bot.send_photo(chat_id=update.effective_chat.id, photo=url,
                                 caption=yaml.dump(cadena, sort_keys=False, default_flow_style=False) )


#datos1=datos[0].to_dict()


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
