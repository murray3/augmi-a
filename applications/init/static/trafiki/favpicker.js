FavPicker = (function(){
	var _self;
	return _self = Ext.extend(Ext.Panel, {
		title: 'Customize',
		onSave: function(){
			//console.log('this', this, this.widget)
			app.onBack();
		},
		initComponent: function(){
			this.rightNavButton = new Ext.Button({
				ui: 'action',
				scope: this,
				handler: this.onSave,
				text: 'Save'
	        });
			
			this.store = new Ext.data.Store({
				model: 'StopList',
				getGroupString : function(record) { return 'Icons'; },
				data: this.data || [
					{ icon: 'briefcase1' },
					{ icon: 'bulb' },
					{ icon: 'bullseye1' },
					{ icon: 'chat_black1' },
					{ icon: 'check_black2' },
					{ icon: 'cloud_black' },
					{ icon: 'code1' },
					{ icon: 'compass3' },
					{ icon: 'cube' },
					{ icon: 'favorites_circle' },
					{ icon: 'globe_black' },
					{ icon: 'headphones' },
					{ icon: 'heart_circle' },
					{ icon: 'home' },
					{ icon: 'hot' },
					{ icon: 'mic' },
					{ icon: 'music1' },
					{ icon: 'nuclear' },
					{ icon: 'phone_black' },
					{ icon: 'photo_black2' },
					{ icon: 'power_on' },
					{ icon: 'reduce' },
					{ icon: 'shield1' },
					{ icon: 'speedometer2' },
					{ icon: 'tree' },
					{ icon: 'tweak' },
					{ icon: 'user_business' },
					{ icon: 'warning_black' }
				]
			});
			
			var picked;
			this.list = new Ext.List({
				activeItem: 2,
				cls: 'favPicker',
				layout: {
					type: 'hbox',
					pack: 'center',
					align: 'stretch'
				},
	            tpl: '<ul><tpl for="."><li class="x-button x-button-plain"><img src="data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==" class="x-icon-mask {icon}"/></li></tpl></ul>',
	            itemSelector: 'li',
	            store: this.store,
				grouped: true,
				singleSelect: true,
				listeners: {
					scope: this,
					afterrender: function(list){ 
						var index = list.store.find('icon', this.widget.o.icon);
						if(index != -1){ list.select(index); } 
					},
					itemtap: function(subList, subIdx, el, e){
						var store  = subList.getStore(),
            				record = store.getAt(subIdx);
						
						console.log(record.get('icon'));
					}
				}
	        });
			
			this.items = [this.list];
			
			_self.superclass.initComponent.call(this);
		}
	});
})();