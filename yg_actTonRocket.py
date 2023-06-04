# meta developer: @yummy_gay
# скитл даун🥰

from .. import loader
import logging

from tgchequeman import exceptions, activate_multicheque, parse_url

logger = logging.getLogger(__name__)

@loader.tds
class yg_actTonRocketModule(loader.Module):
    """Активатор чеков @tonRocketBot которые отправляют как ссылку с автоматической подпиской (и если вы не премиум пользователь автоматически решается капча)"""

    strings = {
        "name": "yg_actTonRocket",
    }

    async def client_ready(self, client, db):
        self.client = client
        await client.send_message('tonRocketBot', '/start')
    
    async def watcher(self, message):
        if message.text and 'https://t.me/tonRocketBot?start=' in message.text:
            code = message.raw_text.split('=')[1]

            bot_url = parse_url("https://t.me/tonRocketBot?start=" + code)

            try:
                await activate_multicheque(
                    client=self.client,
                    bot_url=bot_url,
                    password=None
                )
            except (exceptions.ChequeFullyActivatedOrNotFound, exceptions.PasswordError) as err:
                logger.error(f"Ошибка: {err}")
                # await client.disconnect()
                # sys.exit(1)
            except (exceptions.ChequeActivated,
                    exceptions.ChequeForPremiumUsersOnly,
                    exceptions.CannotActivateOwnCheque) as warn:
                logger.warning(f"Предупреждение: {warn}")
                return
            except exceptions.UnknownError as err:
                logger.error(f"Ошибка: {err}")
                return
            except Exception as err:
                logger.error(f"Ошибка: {err}")

    async def stat_yg_actTonRocketcmd(self, message):
        """проверить работоспособность"""
        await message.edit("<b>Активатор чеков @tonRocketBot работает <emoji document_id=5348140027698227662>🙀</emoji></b>")