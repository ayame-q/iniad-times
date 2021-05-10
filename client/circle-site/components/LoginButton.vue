<template>
	<a class="login-button" v-bind:href="'/auth/google/login?next=' + $route.path">
		<slot>INIADアカウントでログイン</slot>
	</a>
</template>

<script>
export default {
	name: "LoginButton",
};
</script>

<style lang="scss" scoped>
.login-button{
	background-color: #E5F1FF;
	color: $circle-color;
	border: $circle-color solid 3px;
	border-bottom: $circle-color solid 8px;
	font-weight: bold;
	font-size: 1em;
	border-radius: 2em;
	padding: 1.5em 2em;
	display: block;
	width: fit-content;
	margin: 3em auto;
	cursor: pointer;
	&:hover{
		background-color: #FFFFFF;
	}
	&:active{
		margin-top: calc(3em + 5px);
		border-bottom-width: 3px;
	}
}
</style>
