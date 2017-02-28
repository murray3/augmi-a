RouteDetailsView = (function(){
	var _self;
	return _self = Ext.extend(View, {
		scroll: false,
		initComponent: function(){
			this.from = this.points[0];
			this.to = this.points[this.points.length - 1];
			this.title = this.from.title + ' - ' + this.to.title
			
			this.rightNavButton = new Ext.Button({
	            iconCls: "sign_leftright2",
				ui: 'action',
				iconMask: true,
				scope: this,
				handler: this.onFavPick
	        });
			
			/*this.store = new Ext.data.Store({
				model: 'StopList',
				getGroupString : function(record) { return 'Departures'; },
				data: this.data || [
					{ leaving: '11:23', arriving: '12:11', parts: [{ title: 'Bus 15' }, { title: 'Train 372' }] , duration: '0:48' },
					{ leaving: '12:13', arriving: '12:31', parts: [{ title: 'Bus 7' }] , duration: '0:18' },
					{ leaving: '12:38', arriving: '12:59', parts: [{ title: 'Tram 1' }] , duration: '0:21' },
					{ leaving: '13:25', arriving: '13:59', parts: [{ title: 'Bus 5' }, { title: 'Bus 7' }] , duration: '0:24' },
					{ leaving: '14:17', arriving: '14:59', parts: [{ title: 'Train 12' }] , duration: '0:42' },
				]
			});
			
			this.list = new Ext.List({
	            tpl: '<tpl for="."><div class="departureItem" id="{id}"><div class="at">{leaving} »&nbsp;{arriving}</div><div class="points"><img class="icon nodes2" /><ul><tpl for="parts"><li>{title}</li></tpl></ul></div><div class="duration"><img class="icon time" />{duration}</div></div></tpl>',
	            itemSelector: '.departureItem',
	            store: this.store,
				grouped: true,
				listeners: {
					scope: this,
					itemtap: function(subList, subIdx, el, e){
						var store  = subList.getStore(),
            				record = store.getAt(subIdx);
						
					}
				}
	        });*/
		
			
			
			
			//this.items = [this.list]
			this.html = 'This will be a detailed list of the chosen route';
			this.styleHtmlContent = true;
			
			_self.superclass.initComponent.call(this);
		}
	});
})();
