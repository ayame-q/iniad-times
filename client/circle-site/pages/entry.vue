<template>
	<article>
		<div class="eyecatch-wrap">
			<p class="logo"><img src="@/assets/img/logo-square.svg" alt="logo"></p>
			<h2>ENTRY FORM</h2>
			<p class="text">
				Webメディア研究会の活動に興味を持ってくださりありがとうございます。<br>
				ぜひWeb研で活動したい！という方は以下のフォームから入会をお願いします。<br>
				あなたのご参加を心からお待ちしております。
			</p>
		</div>
		<entry-form v-if="isAuthenticated" is-authenticated="is-authenticated"></entry-form>
		<login-button v-if="!isAuthenticated">INIADアカウントでログインして入会</login-button>
	</article>
</template>

<script>
import EntryForm from "@/components/EntryForm";
import LoginButton from "@/components/LoginButton";

export default {
	name: "Entry",
	data() {
		return {
			isAuthenticated: false,
		}
	},
	components: {
		EntryForm,
		LoginButton
	},
	mounted() {
		fetch("/api/is_authenticated")
			.then(response => response.json())
			.then(result => {
				this.isAuthenticated = result.authenticated
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
	}
}

</style>
