<template>
	<div>
		<article v-if="is_member || !is_login">
			<div class="eyecatch-wrap">
				<p class="logo"><img src="@/assets/img/logo-square.svg" alt="logo"></p>
				<h2>ようこそWebメディア研究会へ</h2>
				<p class="text">
					Webメディア研究会へご入会いただきありがとうございます。<br>
					こちらのページにはサークル活動を行う上で知っておいてほしいことや、<br>
					活動をするための準備として行ってほしいことなどがまとめられています。<br>
					必ずご一読をお願いします。
				</p>
			</div>
			<div class="content-wrap" v-if="is_login && is_member">

				<section>
					<h3>Slackワークスペースについて</h3>
					<div class="content">
						<p>
							Webメディア研究会では打ち合わせや連絡に、<br>
							現在大学の授業でも活用されているSlackを利用しております。<br>
							<br>
							また、<b>今後の連絡はすべてSlack上で行います</b>ので、<br>
							重要な連絡を見落とさないよう、PCだけでなく<br>
							スマートフォンにもアプリを入れて通知を設定することをオススメします。<br>
							下の Slack参加 ボタンから参加をお願いします。<br>
							<br>
							<small>また、今後の交流に向けて #自己紹介 チャンネルに簡単な自己紹介を書いていただけますと嬉しいです！</small>
						</p>
						<p><a class="button" v-if="slack_url" v-bind:href="slack_url" target="_blank">Slack参加</a></p>
					</div>
				</section>
				<section>
					<h3>Web新聞「INIAD Times」について</h3>
					<div class="content">
						<section>
							<h4>スタッフ登録のお願い</h4>
							<p>
								Webメディア研究会ではメインの活動として、<br>
								INIAD Timesの記事執筆、編集、開発、運営などを行っています。<br>
								Timesで記事を公開するためにペンネームとスクリーンネーム(URLなどに使われる英数字のID)の登録が必要です。<br>
								好きなペンネームとスクリーンネームを決めていただき、<br>
								下の INIAD Times スタッフ登録 ボタンから登録をお願いします。
							</p>
							<p><a class="button" href="https://iniad-wm.com/staff/profile" target="_blank">INIAD Times スタッフ登録</a></p>
						</section>
						<section>
							<h4>記事執筆・編集について</h4>
							<p>
								記事の執筆、編集などのWeb新聞に関する作業はすべて下のスタッフページより行うことができます。<br>
								いつでも使えるよう、ブックマークをオススメします。<br>
								記事に書きたいことを思いついたら、サークルメンバーであれば誰でもいつでも記事を執筆することができます。<br>
								<br>
								なお、Webメディア研究会ではすべてのメンバーの方になるべく2ヶ月に1本程度以上の記事作成をお願いしたいと考えております。<br>
								ノルマというほど厳しいものではありませんし、できれば…というぐらいのものですので<br>
								ぜひ積極的に記事を書いていただけますととっても嬉しいです。
							</p>
							<p><a class="button" href="https://iniad-wm.com/staff/" target="_blank">INIAD Times スタッフページ</a></p>
						</section>
					</div>
				</section>
				<section>
					<h3>使用ツールについて</h3>
					<div class="content">
						<section>
							<h4>esa.io</h4>
							<p>
								ちょっとしたメモや議事録等の共有のためにesa.ioというツールを使用しています。<br>
								Markdown形式で簡単に文章などを共有でき、複数人で同時編集もできる便利なツールです。<br>
								下のesa.io登録ボタンから登録をお願いします。<br>
								<small>なお、登録後はなるべくわかりやすいスクリーンネームに変更いただけると助かります</small>
							</p>
							<p><a class="button" v-if="esa_url" v-bind:href="esa_url" target="_blank">esa.io登録</a></p>
						</section>
						<section>
							<h4>Discord</h4>
							<p>
								雑談や話し合い、定例会などのためにDiscordというオンラインコミュニケーションツールを使用しています。<br>
								定例会や話し合いなどのイベントの時はもちろん、<br>
								暇なとき、誰かと話したいときなど、気楽に入れるオンライン上の部室のような使い方をしています。<br>
								ぜひ気軽に雑談チャンネルに入り、雑談募集チャンネルで誰かを呼んでみてください。<br>
								下のDiscord登録ボタンから登録をお願いします。<br>
							</p>
							<p><a class="button" v-if="discord_url" v-bind:href="discord_url" target="_blank">Discord登録</a></p>
						</section>
						<section>
							<h4>Google Drive</h4>
							<p>
								主に画像ファイルなどの共有にGoogle Driveの共有フォルダを利用しています。<br>
								下のボタンよりアクセスすることができますので、ご確認ください。
							</p>
							<p><a class="button" v-if="drive_url" v-bind:href="drive_url" target="_blank">Drive共有フォルダ</a></p>
						</section>
					</div>
				</section>
				<section>
					<h3>定例会などの活動について</h3>
					<div class="content">
						<p>
							現在、原則として月2回（2020年度秋学期は毎月第2, 第4木曜日 20:00〜）<br>
							定例会としてサークルのいろいろなことを決める話し合いを行っています。<br>
							学期はじめにアンケートにて、その学期内の定例会の日程を決めますのでご協力ください。<br>
							なお、春休みなどの長期休暇期間内は毎回アンケート調査などによって日程を決定し<br>
							同様に月2回程度を目安に定例会を行っております。<br>
							<br>
							また、長期休暇期間内を中心に「もくもく会」という<br>
							雑談しながら、それぞれ好きな作業やお勉強、ゲーム、などなど、<br>
							それぞれ自由に有意義に時間を過ごそう！って感じのイベントを行っています。<br>
							他にも、対面活動が可能になりましたら、キャンパスの教室などを活用し<br>
							Webプログラミングやデザインの勉強会の開催を予定しております。<br>
							<br>
							基本的にこれらのイベントの告知はすべてSlackの #総合 チャンネルで行っております。<br>
							ぜひご参加ください。
						</p>
					</div>
				</section>
				<section>
					<h3>活動内容アンケートについて</h3>
					<div class="content">
						<p>
							今後ご一緒にいろいろな活動をしていくに当たって、<br>
							お手数ですが下のボタンより、<br>
							サークルでどのような活動をしたいかを調査するアンケートにご協力をお願いします。
						</p>
						<p><a class="button" v-if="questionnaire_url" v-bind:href="questionnaire_url" target="_blank">アンケート</a></p>
					</div>
				</section>
			</div>
		</article>
		<login-button v-if="!is_login">INIADアカウントでログインして表示</login-button>
		<article v-if="is_login && !is_member" class="error">
			<h2>Error!</h2>
			<p>
				Webメディア研究会に入会いただいた方向けのページです。<br>
				<nuxt-link to="/entry">入会はこちら</nuxt-link>
			</p>
		</article>
	</div>
</template>

<script>
export default {
	name: "Tutorial",
	data() {
		return {
			is_login: false,
			is_member: false,
			slack_url: null,
			esa_url: null,
			discord_url: null,
			drive_url: null,
			questionnaire_url: null,
		}
	},
	mounted() {
		fetch("/api/tutorial")
			.then(response => response.json())
			.then(result => {
				console.log(result)
				this.is_login = result.is_login
				this.is_member = result.is_member
				this.slack_url = result.slack_url
				this.esa_url = result.esa_url
				this.discord_url = result.discord_url
				this.drive_url = result.drive_url
				this.questionnaire_url = result.questionnaire_url
			})
	}
};
</script>

<style lang="scss" scoped>
.eyecatch-wrap{
	width: 100vw;
	height: calc(100vw / 1920 * 493);
	color: #FFFFFF;
	background-image: url("~/assets/img/entry-eyecatch.jpg");
	background-size: cover;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
	h2{
		margin: 0.5em 0;
	}
	.logo img{
		width: 7vw;
		border: #FFFFFF 2px solid;
	}
	.text{
		line-height: 1.8;
		font-size: 0.8em;
	}
}
.content-wrap > section{
	margin: 2em auto;
	h3{
		font-size: 26px;
	}
	h4{
		font-size: 22px;
		margin-bottom: 0.2em;
	}
	width: 1000px;
	max-width: 100vw;
	.content{
		background-color: rgba($circle-color, 0.2);
		width: 100%;
		padding: 40px 30px;
		font-size: 18px;
		section{
			margin-top: 2em;
			&:first-child{
				margin-top: 0;
			}
		}
	}
	a.button{
		text-align: center;
		cursor: pointer;
		display: block;
		padding: 0.5em 1.25em;
		border-radius: 14px;
		margin: 0;
		margin-top: 15px;
		width: fit-content;
		background-color: #FFFFFF;
		color: $circle-color;
		border-bottom: $circle-color 0.3em solid;
	}
}

.error{
	text-align: center;
	display: flex;
	flex-direction: column;
	justify-content: center;
	font-size: 2vw;
	height: 80vh;
}

</style>
