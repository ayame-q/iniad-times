<template>
	<form>
		<section class="profile-wrap">
			<h3>Profile</h3>
			<div class="form-section">
				<div class="line name-line">
					<p>
						<label for="form-family-name">姓</label>
						<input type="text" id="form-family-name" v-model="name" placeholder="東洋">
					</p>
					<p>
						<label for="form-given-name">名</label>
						<input type="text" id="form-given-name" v-model="name" placeholder="太郎">
					</p>
				</div>
				<div class="line name-line">
					<p>
						<label for="form-family-name-ruby">フリガナ(姓)</label>
						<input type="text" id="form-family-name-ruby" v-model="ruby" placeholder="トウヨウ">
					</p>
					<p>
						<label for="form-given-name-ruby">フリガナ(名)</label>
						<input type="text" id="form-given-name-ruby" v-model="ruby" placeholder="タロウ">
					</p>
				</div>
				<p>
					<label for="form-mail">学内メールアドレス</label>
					<input type="email" id="form-mail" v-model="mail" placeholder="s1f100009999@iniad.org">
				</p>
				<div class="line">
					<p class="student-id">
						<label for="form-student-id">学籍番号</label>
						<input type="email" id="form-student-id" v-model="studentId" placeholder="1F10000999">
					</p>
					<p class="grade">
						<label for="form-grade">学年</label>
						<input type="number" id="form-grade" v-model="grade" placeholder="1">
					</p>
				</div>
				<div class="line">
					<p>
						<label for="form-cource">コース</label>
						<select id="form-cource" v-model="course">
							<option v-bind:value="null" selected>なし</option>
							<option value="engineering">エンジニアリング</option>
							<option value="design">デザイン</option>
							<option value="business">ビジネス</option>
							<option value="civil-system">シビルシステム</option>
						</select>
					</p>
					<p class="cource-detail">1年生・未所属の方は希望するコースがもしあれば<br>選択してください。</p>
				</div>
			</div>
		</section>
		<section class="questionnaire-wrap">
			<h3>Questionnaire</h3>
			<div class="form-section">
				<div>
					<p>
						<label for="form-interested-in">
							このサークルで興味がある、またはやってみたい内容を選んでください<br>
							<span style="font-size: 0.9em">※複数選択◎</span>
						</label>
					</p>
					<ul id="form-interested-in">
						<li class="checkbox-wrap">
							<input type="checkbox" id="form-interested-in-article" v-model="interestedIn" value="writing">
							<label for="form-interested-in-article">記事作成</label>
						</li>
						<li class="checkbox-wrap">
							<input type="checkbox" id="form-interested-in-movie" v-model="interestedIn" value="movie">
							<label for="form-interested-in-movie">動画編集</label>
						</li>
						<li class="checkbox-wrap">
							<input type="checkbox" id="form-interested-in-system" v-model="interestedIn" value="system">
							<label for="form-interested-in-system">システム</label>
						</li>
						<li class="checkbox-wrap">
							<input type="checkbox" id="form-interested-in-design" v-model="interestedIn" value="design">
							<label for="form-interested-in-design">デザイン</label>
						</li>
					</ul>
				</div>
			</div>
		</section>
		<p class="submit-wrap"><input type="submit" value="入会"></p>
	</form>
</template>

<script>
export default {
	name: "EntryForm",
	data() {
		return {
			name: null,
			ruby: null,
			mail: null,
			studentId: null,
			grade: null,
			course: null,
			interestedIn: [],
		}
	}
};
</script>

<style lang="scss" scoped>

form{
	margin: 5vw auto;
	width: 550px;
	max-width: 100vw;
	display: flex;
	flex-direction: column;
	align-items: center;
	color: #044088;
	section{
		margin: 1em;
		h3{
			font-size: 24px;
		}
		width: 100%;
		.form-section{
			background-color: rgba($circle-color, 0.4);
			width: 100%;
			padding: 6% 8%;
			font-size: 14px;
			p{
				display: flex;
				flex-direction: column;
				&.student-id{
					width: 78%;
				}
				&.grade{
					width: 18%;
					position: relative;
					z-index: 1;
					&::after{
						z-index: 2;
						content: "年";
						position: absolute;
						font-size: 12px;
						right: 6px;
						bottom: 14px;
					}
					input{
						padding-right: 1.5em;
					}
				}
				&.cource-detail{
					margin-left: 1em;
					margin-right: auto;
					font-size: 0.8em;
				}
			}
			.line{
				display: flex;
				justify-content: space-between;
				align-items: flex-end;
				&.name-line{
					> p{
						width: 48%;
					}
				}
			}
			ul{
				list-style: none;
				margin-top: 1.2em;
				padding: 0;
				display: flex;
				justify-content: space-between;
				li{
					flex-basis: 22%;
				}
			}
		}
	}
	.submit-wrap{
		margin-top: 1.5em;
	}
}

input, select, textarea{
	font-family: inherit;
	margin-top: 5px;
	margin-bottom: 10px;
	font-size: 1.1em;
	padding: 0.4em 0.8em;
	box-sizing: border-box;
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	border: none;
	border-radius: 8px;
	width: calc(100%);
	background-color: white;
	color: #044088;
	&::placeholder{
		color: rgba(#044088, 0.2);
	}

	&[type=submit]{
		background-color: #E5F1FF;
		color: $circle-color;
		border: $circle-color solid 3px;
		border-bottom: $circle-color solid 8px;
		font-weight: bold;
		font-size: 18px;
		border-radius: 2em;
		padding: 0.5em 2em;
		display: block;
		width: fit-content;
		margin-left: auto;
		margin-right: 0;
		cursor: pointer;
		&:hover{
			background-color: #FFFFFF;
		}
	}
	&:disabled{
		background-color: lightgray;
	}
}

.checkbox-wrap{
	position: relative;
	input[type=checkbox]{
		cursor: pointer;
		z-index: 2;
		position: absolute;
		top: 0;
		width: 100%;
		height: 2.85em;
		margin: 0;
		background-color: $circle-color;
		transition: all 0.3s;
		&:checked+label{
			cursor: pointer;
			color: #FFFFFF;
			margin-top: 0.25em;
			margin-bottom: -0.25em;
		}
		&:not(:checked){
			&::after{
				cursor: pointer;
				content: "";
				z-index: 1;
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 2.5em;
				border-radius: 8px;
				background-color: #FFFFFF;
			}
		}
	}
	label{
		cursor: pointer;
		transition: all 0.3s;
		position: relative;
		z-index: 2;
		line-height: 2.8;
		text-align: center;
		width: 100%;
		display: block;
		&:checked{
			color: #FFFFFF;
		}
	}
}

select{
	margin: 0;
	padding: 0.6em 0.8em;
	padding-right: 38px;
	background-image:
		linear-gradient(45deg, transparent 50%, rgba($circle-color, 0.4) 50%),
		linear-gradient(135deg, rgba($circle-color, 0.4) 50%, transparent 50%);
	background-position:
		calc(100% - 20px) 50%,
		calc(100% - 15px) 50%;
	background-size:
		5px 5px,
		5px 5px;
	background-repeat: no-repeat;

}
</style>
