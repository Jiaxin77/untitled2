



var person=['层次分析专家','可用性测试被试人员'];
/*
var Index=[
	{
		id:1,
		name:"软件人机界面",
		FirstList:
		[
		 {
			id:11,
			listTitle:"易学性",
			selected:
			[
				{
					id:111,
					listTitle:"一致性",
					method:"启发式评估法"
				},
				{
					id:112,
					listTitle:"认知负荷",
					method:"启发式评估法"
				}
			]
		 },
		 {
			id:12,
			listTitle:"容错性",
			selected:
			[
				{
					id:121,
					listTitle:"防止犯错",
					method:"可用性测试"
				}
			]
		 },
		 {
			id:13,
			listTitle:"易用性",
			selected:
			[
				{
					id:132,
					listTitle:"适用性",
					method:"可用性测试"
				}
			]
		 }

		]

	},
	{
		id:2,
		name:"系统任务流程",
		FirstList:
		[
		 {
			id:21,
			listTitle:"有效性",
			selected:
			[
				{
					id:211,
					listTitle:"功能完备性",
					method:"启发式评估法"
				},
				{
					id:212,
					listTitle:"任务有效性",
					method:"启发式评估法"
				}
			]
		 },
		 {
			id:22,
			listTitle:"效率",
			selected:[]
	
		}
		]
	}
	];
*/
	var IndexInform={
		indexName:"",
		EvaMethod:"",
		EvaObject:"",
		dataSource:"",
		dataDeal:""
	};

	


var app=new Vue({
	el:'#app',
	data:{
		people:person,
		myIndex:Index,
		IndexInfo:IndexInform,
		IndexBox:[],
        Assess:assess

	},
		//在页面刚加载时就执行的函数——Vue生命周期
		mounted()
		{
			this.initData();
		},
		methods:{
			initData:function()
			{
				for (var i=0;i<this.myIndex.length;i++)
				{
					for(var j=0;j<this.myIndex[i].FirstList.length;j++)
					{
						for(var z=0;z<this.myIndex[i].FirstList[j].selected.length;z++)
						{
							var item={};
							item.indexName=this.myIndex[i].FirstList[j].selected[z].listTitle;
							item.EvaMethod=this.myIndex[i].FirstList[j].selected[z].method;
							item.EvaObject=this.myIndex[i].name+"的"+this.myIndex[i].FirstList[j].listTitle;
							if(item.EvaMethod=="启发式评估法")
							{
								/*这部分之后可以调用函数 根据评估方法的数据获得*/
								item.dataSource="启发式评估表格";
								item.dataDeal="收集数据";
							}
							else if(item.EvaMethod=="可用性测试")
							{
								item.dataSource="问卷调查";
								item.dataDeal="整理统计";
							}
							else
							{
								item.dataSource="暂未记录";
								item.dataDeal="暂未记录";
							}

							this.IndexBox.push(item);

						}
					}
				}
				
			}

		}
	})

