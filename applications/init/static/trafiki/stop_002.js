StopView = (function(){
	var _self;
	return _self = Ext.extend(View, {
		scroll: false,
		initComponent: function(){
			this.title = this.o.title || "";
			
			this.rightNavButton = new Ext.Button({
	            iconCls: "star",
				ui: 'action',
				iconMask: true,
				scope: this,
				handler: this.onFavPick
	        });
			
			this.store = new Ext.data.Store({
				model: 'StopList',
				getGroupString : function(record) { return 'Realtime departures'; },
				data: this.data || [
					{ line: 1, towards: "Fisherman's Wharf", at: 2 },
					{ line: 3, towards: "Alcatraz", at: 7, color: '#0aa', mot: 'bus' },
					{ line: 7, towards: "Palo Alto", at: 12, color: '#a0a', mot: 'bus' }
				]
			});
			
			this.list = new Ext.List({
	            tpl: '<tpl for="."><div class="realtimeItem" id="{id}"><div class="line"><div class="mot {mot}" style="background: {color};"></div><div class="lineNumber">{line}</div></div><div class="towards">{towards}</div><div class="at">{at}</div></div></tpl>',
	            itemSelector: '.realtimeItem',
	            store: this.store,
				grouped: true,
				listeners: {
					scope: this,
					itemtap: function(subList, subIdx, el, e){
						var store  = subList.getStore(),
            				record = store.getAt(subIdx);
							
						//console.log(record.get('title'))
						//this.callback(null, record.get('sid'));
						//console.log('t', this);
					}
				}
	        });
		
			
			this.buttons = new Ext.Panel({
				cls: 'optionbuttons',
				layout: {
					type: 'hbox',
                    pack: 'center',
					align: 'stretch'
                },
                defaults: {
					xtype: 'button',
                    iconMask: true,
                    ui: 'plain',
					iconAlign: 'top',
					scope: this
                },
				items: [
				{ iconCls: 'locate', text: 'Maps', handler: this.onMaps },
				{ iconCls: 'list', text: 'Timetable' },
				{ iconCls: 'bullseye1', text: 'Go from here', handler: this.onGo.bind(this, ['from'], true) },
				{ iconCls: 'forward_black', text: 'Go to here', handler: this.onGo.bind(this, ['to'], true) }
				]
			});
			
			this.items = [this.buttons, this.list]
			
			_self.superclass.initComponent.call(this);
		},
		
		onFavPick: function(){
			app.fireEvent('open', new FavPicker({ o: this.o, widget: this.widget }));
		},
		onMaps: function(){ app.fireEvent('open', m = new MapView({ title: 'Map', o: this.o })) },
		onGo: function(el, e, type){
			var opposite = { from: 'to', to: 'from' },
				editFn = { from: 'push', to: 'unshift' },
				me = this;
				
			app.fireEvent('open', new DashboardView({
				title: s['going_' + opposite[type]],
				editable: false,
				widgets: widgets,
				onTapCallback: function(widget){
					var arr = [new Widget({ o: me.o })];
					arr[editFn[type]](widget);
					app.getRoute(arr);
				}
			}));
		},
		
		
	});
})();

Ext.regModel('IconButton', {
    fields: [
        { name: 'title',      type: 'string' },
		{ name: 'sid',        type: 'string' },
    ]
});
