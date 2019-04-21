
/*
	var AllModel=[
	{
		id:1,
		name:"历史模板名称1",
		InShort:"历史模板1一句话描述一句话描述",
		type:"history"
	},
	{
		id:2,
		name:"综合模板名称2",
		InShort:"综合模板2一句话描述一句话描述",
		type:"coll"
	},
	{
		id:3,
		name:"表单名称3",
		InShort:"表单3一句话描述一句话描述",
		type:"list"	
	},
	{
		id:4,
		name:"表单名称4",
		InShort:"表单3一句话描述一句话描述",
		type:"list"
	},
	{
		id:5,
		name:"历史模板名称1",
		InShort:"历史模板1一句话描述一句话描述",
		type:"history"
	},
	{
		id:6,
		name:"历史模板历史2",
		InShort:"历史模板2一句话描述一句话描述",
		type:"history"
	},
	{
		id:7,
		name:"综合模板3",
		InShort:"综合模板3一句话描述一句话描述",
		type:"coll"
	},
	{
		id:8,
		name:"历史模板4",
		InShort:"历史模板3一句话描述一句话描述",
		type:"history"
	}

	]; */



	var app=new Vue({
		el:'#app',
		data:{
			Models:AllModel,
            chooseModel:{begin:'true'},
            User:User

		},
		methods:{
			/*点击从空白处新建评估弹框*/
			newFromWhite:function()
			{

				if(document.getElementById('shadow').style.visibility=='hidden'&&document.getElementById('newEvaBox').style.visibility=='hidden')
				{
					document.getElementById('shadow').style.visibility='visible';
					document.getElementById('newEvaBox').style.visibility='visible';
				}
			},
			closeNewBox:function()
			{

					document.getElementById('shadow').style.visibility='hidden';
					document.getElementById('newEvaBox').style.visibility='hidden';
                    document.getElementById('newModelBox').style.visibility='hidden';
				location.href='/newEva/';
			},
			submitForm:function()
			{
				if (document.getElementById('EvaNameInput').value!=null)
				{
					document.BlankEva.submit();

				}
				else
				{
					alert("名称不能为空！")
				}
			},
			changeList:function()
			{
				document.getElementById('AllModelEvaluation').style.visibility="hidden";
				document.getElementById('ListEvaluation').style.visibility="visible";
				document.getElementById('CollEvaluation').style.visibility="hidden";
				document.getElementById('HistoryEvaluation').style.visibility="hidden";
			},
			changeHistory()
			{
				document.getElementById('AllModelEvaluation').style.visibility="hidden";
				document.getElementById('ListEvaluation').style.visibility="hidden";
				document.getElementById('CollEvaluation').style.visibility="hidden";
				document.getElementById('HistoryEvaluation').style.visibility="visible";	
			},
			changeColl:function()
			{
				document.getElementById('AllModelEvaluation').style.visibility="hidden";
				document.getElementById('ListEvaluation').style.visibility="hidden";
				document.getElementById('CollEvaluation').style.visibility="visible";
				document.getElementById('HistoryEvaluation').style.visibility="hidden";
			},
			changeAll:function()
			{
				document.getElementById('AllModelEvaluation').style.visibility="visible";
				document.getElementById('ListEvaluation').style.visibility="hidden";
				document.getElementById('CollEvaluation').style.visibility="hidden";
				document.getElementById('HistoryEvaluation').style.visibility="hidden";
			},
            newFromModel:function(model)
			{
				console.log(this.chooseModel)
				this.$set(this.chooseModel,'AssessId',model.AssessId);
				this.$set(this.chooseModel,'ModelId',model.ModelId)
				this.$set(this.chooseModel,'name',model.name);
				if(model.type=='coll')
				{
					this.$set(this.chooseModel,'type', '综合');
				}
				else if(model.type=='list')
				{
					this.$set(this.chooseModel,'type','单一问卷');
				}


				if(document.getElementById('shadow').style.visibility=='hidden'&&document.getElementById('newModelBox').style.visibility=='hidden')
				{
					document.getElementById('shadow').style.visibility='visible';
					document.getElementById('newModelBox').style.visibility='visible';
				}

			},
            submitFromModel:function()
            {
                axios.post('/newEvaFromModel/',
						JSON.stringify({
						Model:this.chooseModel
                            ////////////////底下未改呢！

					}))
						.then(function(response){
							console.log(response);
							//window.location.href='/chooseEva/'
						})
						.catch(function(error){
							console.log(error);
						})
            }


		}
	})


