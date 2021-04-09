from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
import re, secrets, string, os

def send_initial_mail(email):
    message_text = f"""Webメディア研究会 新規メンバーの皆さま

はじめまして。Webメディア研究会代表の立松あやめと申します。

この度はWebメディア研究会にご入会いただきありがとうございます。
皆さまと一緒に活動できることを大変嬉しく思っております。


さて、早速ですが、
以下のURLにあります新規入会者向け案内ページに
Webメディア研究会でサークル活動を行う上で、知っておいてほしいことや
活動をするための準備として行ってほしいことなどがまとめられています。
必ずご一読いただけますようお願いします。

-------------------------------------

Webメディア研究会 新規入会者向け案内ページ
https://about.iniad-wm.com/tutorial

-------------------------------------


なお、上記ページでも案内されておりますが
Webメディア研究会では打ち合わせや連絡に
現在大学の授業でも活用されているSlackを利用しております。

お手数ですが、
{os.environ.get("CIRCLE_TUTORIAL_SLACK_URL")}
よりSlackへの参加をお願いします。
なお、その際必ずINIADメールアドレスで登録してください。


また、今後の連絡はすべて上記Slackにて行いますので
可能であればスマートフォン等にSlackのアプリを入れていただき、
通知を見落とさないようにしていただけると幸いです。


末筆ながら、今後はWebメディア研究会の一員としてぜひよろしくお願いします。
皆さまがサークル活動を楽しんでいただき、有意義なものと感じていただけたら幸いです。


Webメディア研究会
代表 立松 あやめ
    """

    message_html = f"""<p>Webメディア研究会 新規メンバーの皆さま</p>

<p>はじめまして。Webメディア研究会代表の立松あやめと申します。</p>

<p>この度はWebメディア研究会にご入会いただきありがとうございます。<br>
皆さまと一緒に活動できることを大変嬉しく思っております。</p>
<br>

<p>さて、早速ですが、<br>
以下のURLにあります新規入会者向け案内ページに<br>
Webメディア研究会でサークル活動を行う上で、知っておいてほしいことや<br>
活動をするための準備として行ってほしいことなどがまとめられています。<br>
必ずご一読いただけますようお願いします。</p>

<p style="font-size: 1.2em;">-------------------------------------<br>
<br>
Webメディア研究会 新規入会者向け案内ページ<br>
<a href="https://about.iniad-wm.com/tutorial">https://about.iniad-wm.com/tutorial</a><br>
<br>
-------------------------------------</p>
<br>

<p>なお、上記ページでも案内されておりますが<br>
Webメディア研究会では打ち合わせや連絡に<br>
現在大学の授業でも活用されているSlackを利用しております。</p>

<p>お手数ですが、<br>
<a href="{os.environ.get("CIRCLE_TUTORIAL_SLACK_URL")}">{os.environ.get("CIRCLE_TUTORIAL_SLACK_URL")}</a></br>
よりSlackへの参加をお願いします。<br>
なお、その際必ずINIADメールアドレスで登録してください。</p>
<br>

<p>また、今後の連絡はすべて上記Slackにて行いますので<br>
可能であればスマートフォン等にSlackのアプリを入れていただき、<br>
通知を見落とさないようにしていただけると幸いです。</p>
<br>

<p>末筆ながら、今後はWebメディア研究会の一員としてぜひよろしくお願いします。<br>
皆さまがサークル活動を楽しんでいただき、有意義なものと感じていただけたら幸いです。</p>
<br>

<p>Webメディア研究会<br>
代表 立松 あやめ</p>
    """

    subject = "【Webメディア研究会】ご入会ありがとうございます"
    from_email = 'info@iniad-wm.com'
    to_emails = [email]
    msg = EmailMultiAlternatives(subject, message_text, from_email, to_emails)
    msg.attach_alternative(message_html, "text/html")
    msg.send()
    print(f"{email} へ入会メールを送信しました。")
