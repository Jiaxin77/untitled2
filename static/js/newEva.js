

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

	];

/*
	var AllComModel=[
	{
		id:1,
		name:"综合模板1",
		InShort:"综合模板1一句话描述一句话描述"
	},
	{
		id:2,
		name:"综合模板2",
		InShort:"综合模板2一句话描述一句话描述"
	},
	{
		id:3,
		name:"综合模板3",
		InShort:"综合模板3一句话描述一句话描述"
	},
	{
		id:4,
		name:"综合模板4",
		InShort:"综合模板3一句话描述一句话描述"
	}
	];

	var AllHisModel=[
	{
		id:1,
		name:"历史模板1",
		InShort:"历史模板1一句话描述一句话描述"
	},
	{
		id:2,
		name:"历史模板2",
		InShort:"历史模板2一句话描述一句话描述"
	},
	{
		id:3,
		name:"历史模板3",
		InShort:"历史模板3一句话描述一句话描述"
	},
	{
		id:4,
		name:"历史模板4",
		InShort:"历史模板4一句话描述一句话描述"
	}
	];
	*/

	var app=new Vue({
		el:'#app',
		data:{
			Models:AllModel

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

				if(document.getElementById('shadow').style.visibility=='visible'&&document.getElementById('newEvaBox').style.visibility=='visible')
				{
					document.getElementById('shadow').style.visibility='hidden';
					document.getElementById('newEvaBox').style.visibility='hidden';
				}	
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
			changeList()
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
			changeColl()
			{
				document.getElementById('AllModelEvaluation').style.visibility="hidden";
				document.getElementById('ListEvaluation').style.visibility="hidden";
				document.getElementById('CollEvaluation').style.visibility="visible";
				document.getElementById('HistoryEvaluation').style.visibility="hidden";
			},
			changeAll()
			{
				document.getElementById('AllModelEvaluation').style.visibility="visible";
				document.getElementById('ListEvaluation').style.visibility="hidden";
				document.getElementById('CollEvaluation').style.visibility="hidden";
				document.getElementById('HistoryEvaluation').style.visibility="hidden";
			}

		}
	})


