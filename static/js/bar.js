// 路径配置
    require.config({
        paths: {
            echarts: 'http://echarts.baidu.com/build/dist'
        }
    });
    // 使用
    require(
        [
            'echarts',
            'echarts/chart/bar', // 使用柱状图就加载bar模块，按需加载
            'echarts/chart/pie',
        ],
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
            var myChart = ec.init(document.getElementById('general')); 
            var myChart_lang = ec.init(document.getElementById('lang')); 
            var mydata0=[];
            var mydata1=[];
            var pie_legend1=[];
            var pie_legend2=[];
            var pie_data1=[];
            var pie_data2=[];

            option = {
                title : {
                    text: 'VS',
                    subtext: 'data from github, stackoverflow, reddit',
                    x:'center'
                },
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:["angular/angular", "emberjs/ember.js"],
                    x : 'left',
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: false},
                        dataView : {show: false, readOnly: false},
                        magicType: {show: false, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'value',
                        boundaryGap : [0, 0.01]
                    }
                ],
                yAxis : [
                    {
                        type : 'category',
                        data : ['watcher','stars','forks','open_issues','contributors','stackoverflow']
                    }
                ],
                series : [
                    {
                        name:"angular/angular",
                        type:'bar',
                        
                    },
                    {
                        name:"emberjs/ember.js",
                        type:'bar',
                        
                    }
                ]
            };
            option_lang = {
                title : {
                    text: "angular/angular language",
                    subtext: 'from github',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient : 'vertical',
                    x : 'left',
                    data:['直接访问','邮件营销','联盟广告','视频广告','搜索引擎']
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: false},
                        dataView : {show: false, readOnly: false},
                        magicType : {
                            show: false, 
                            type: ['pie', 'funnel'],
                            option: {
                                funnel: {
                                    x: '25%',
                                    width: '50%',
                                    funnelAlign: 'left',
                                    max: 1548
                                }
                            }
                        },
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series : [
                    {
                        name:'访问来源',
                        type:'pie',
                        radius : '55%',
                        center: ['50%', '60%'],
                        data:[
                            {value:335, name:'直接访问'},
                            {value:310, name:'邮件营销'},
                            {value:234, name:'联盟广告'},
                            {value:135, name:'视频广告'},
                            {value:1548, name:'搜索引擎'}
                        ]
                    }
                ]
            };


            
            $.ajax({  
                    url: "/diffdata?onerepo_owner=angular&onerepo_name=angular&tworepo_owner=emberjs&tworepo_name=ember.js",
                    dataType:"json", 
                    async:false,
                    success:function(point){
                      var obj=eval(point);
                      mydata0 = [obj.onerepo.watchers_count, obj.onerepo.stargazers_count, obj.onerepo.forks_count, obj.onerepo.open_issues, obj.onerepo.repo_ctb_count, obj.onerepo.sof_count];
                      mydata1 = [obj.tworepo.watchers_count, obj.tworepo.stargazers_count, obj.tworepo.forks_count, obj.tworepo.open_issues, obj.tworepo.repo_ctb_count, obj.tworepo.sof_count];
                      var language1 = obj.onerepo.language;
                      for (var key in language1) {
                          pie_legend1.push(key);
                          pie_data1.push({value:language1[key], name:key});
                      };

                   },  
                    error: function(){alert('error!')},
            });
            option.series[0].data = mydata0;
            option.series[1].data = mydata1;
            option_lang.legend.data = pie_legend1;
            option_lang.series[0].data = pie_data1;
            // // 为echarts对象加载数据 
            myChart.setOption(option);
            myChart_lang.setOption(option_lang);
        }
    );