<template>
	<div class="message">
		<h2>ご入会ありがとうございます</h2>
		<p>ありがとうございます！入会受付が完了しました。</p>
		<p>メールをお送りしましたので、ご確認ください！</p>
		<p style="margin: 0.3em 0"><small>なお、万が一1日経ってもメールが届かない場合は<a href="mailto:info@iniad-wm.com">info@iniad-wm.com</a>までご連絡ください。</small></p>
		<p style="margin: 2em; font-size: 0.7em"><nuxt-link to="/">トップへ戻る</nuxt-link></p>
	</div>
</template>

<script>
export default {
	name: "EntriedMessage",
};
</script>

<style lang="scss" scoped>
.message{
	color: #044088;
	text-align: center;
	margin: 5em auto;
	h2{
		margin: 0.5em 0;
	}
}
</style>
