

	// var AllAssess=[
	// 	{
	// 		id:1,
	// 		name:"评估名称1",
	// 		person:"曲丽丽",
	// 		InShort:"我是评估1一句话描述",
	// 		BeginTime:"2018-06-16 14:03",
	// 		process:90,
	// 		condition:"ing"
	// 	},
	// 	{
	// 		id:2,
	// 		name:"评估名称2",
	// 		person:"丁程鑫",
	// 		InShort:"我是评估2一句话描述",
	// 		BeginTime:"2018-06-18 17:03",
	// 		process:30,
	// 		condition:"ing"
	// 	},
	// 	{
	// 		id:3,
	// 		name:"评估名称3",
	// 		person:"马嘉祺",
	// 		InShort:"我是评估3一句话描述",
	// 		BeginTime:"2018-03-18 17:03",
	// 		process:100,
	// 		condition:"End"
	// 	},
	// 	{
	// 		id:4,
	// 		name:"评估名称3",
	// 		person:"李汶翰",
	// 		InShort:"我是评估4一句话描述",
	// 		BeginTime:"2017-03-18 17:03",
	// 		process:100,
	// 		condition:"End"
	// 	}
	// ]


	var app=new Vue({
		el:'#app',
		data:{
			assess:AllAssess,
			now:"All"
		},

		methods:{

	 			lookMore:function(data)
				{
					
					var id=data.id+this.now+"_more";
					console.log("get"+data.id+this.now+"_more");
					if(document.getElementById(id).style.visibility=='hidden')
					{
						document.getElementById(id).style.visibility="visible";
					}
					else
					{
						document.getElementById(id).style.visibility="hidden";
					}
		
				},
				getMoreId:function(data,txt)
				{	
					console.log(data.id+txt+"_more");
					return data.id+txt+"_more"

				},
				changeAll:function()
				{//选择显示所有评估方案
					var moreInfo=document.getElementsByClassName('moreInfo');
					for(var i=0;i<moreInfo.length;i++)
					{
						moreInfo[i].style.visibility="hidden";
					}
					document.getElementById('IngEvaluation').style.visibility="hidden";
					document.getElementById('EndEvaluation').style.visibility="hidden";
					document.getElementById('AllEvaluation').style.visibility="visible";
					this.now="All";
					console.log("now"+this.now);
				},
				changeIng:function()
				{
					var moreInfo=document.getElementsByClassName('moreInfo');
					for(var i=0;i<moreInfo.length;i++)
					{
						moreInfo[i].style.visibility="hidden";
					}
					document.getElementById('IngEvaluation').style.visibility="visible";
					document.getElementById('EndEvaluation').style.visibility="hidden";
					document.getElementById('AllEvaluation').style.visibility="hidden";
					this.now="Ing";
					console.log("now"+this.now);
				},
				changeEnd:function()
				{
					var moreInfo=document.getElementsByClassName('moreInfo');
					for(var i=0;i<moreInfo.length;i++)
					{
						moreInfo[i].style.visibility="hidden";
					}

					document.getElementById('IngEvaluation').style.visibility="hidden";
					document.getElementById('EndEvaluation').style.visibility="visible";
					document.getElementById('AllEvaluation').style.visibility="hidden";
					this.now="End";
					console.log("now"+this.now);
				},
				getProcessbar:function(data)
				{
					return data.process;
				},
                getFillEva:function (EvaData)
                {
                    //因为是向后台get，所以在这里做跳转
                    console.log(EvaData)
                    axios.get('http://127.0.0.1:8000/getFillAssess/',{
                        params:{
                            assess:EvaData.id
                        }
                    })
                        .then(function(response){
                            console.log(response);
                           window.location.href='/getFillAssess/?assess='+EvaData.id;
                        })
                        .catch(function(error) {
                            console.log(error);
                        })

                },
				deleteEva:function(EvaData)
				{
					axios.post('http://127.0.0.1:8000/deleteAssess/',
						JSON.stringify({
						assess:EvaData.id

					}))
						.then(function(response){
							console.log(response);
							window.location.href='/chooseEva/'
						})
						.catch(function(error){
							console.log(error);
						})

				},
                getid(eva)
                {
                    return eva.id;
                }


		}
	})
