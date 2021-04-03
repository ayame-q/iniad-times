<template>
	<article class="index">
		<eye-catch></eye-catch>

		<promotion-video></promotion-video>

		<activities></activities>

		<news-list-simple></news-list-simple>

		<ask-or-join></ask-or-join>

		<circle-info></circle-info>
	</article>
</template>

<script>
import EyeCatch from "@/components/EyeCatch";
import PromotionVideo from "@/components/PromotionVideo";
import Activities from "@/components/Activities";
import NewsListSimple from "@/components/NewsListSimple";
import AskOrJoin from "@/components/AskOrJoin";
import CircleInfo from "@/components/CircleInfo";

export default {
	components: {
		EyeCatch,
		PromotionVideo,
		Activities,
		NewsListSimple,
		AskOrJoin,
		CircleInfo
	}
};
</script>

<style lang="scss" scoped>

</style>
