SearchView = (function(){
	var _self;
	return _self = Ext.extend(View, {
		initComponent: function(){
			this.title = s['going_' + this.type] || s['show_stop'];
			
			this.searchField = new Ext.form.SearchField({
				placeHolder: 'Stop name',
				autoFocus: false,
				listeners: {
					scope: this,
					keyup: function(field){ 
						var val = field.getValue();
						if (!val) {
							this.store.clearFilter();
						}
						else {
							var re = new RegExp("\\b" + val, "i");
							this.store.filterBy(function(record){
								return re.test(record.get('title'));
							});
						}
					},
					change: function(){ console.log('change'); }
				}
			});
			
			this.dockedItems = {
	            xtype: 'toolbar',
	            dock: 'top',
	            items: [{xtype: 'spacer'}, this.searchField, {xtype: 'spacer'}]
	        }
			
			this.store = new Ext.data.Store({
				model: 'StopList',
				data: this.data || [
					{ sid: 3, title: "Alcatraz" },
					{ sid: 1, title: "Fisherman's Wharf" },
					{ sid: 7, title: "Palo Alto" }
				]
			});
			
			this.list = new Ext.List({
	            tpl: '<tpl for="."><div class="menuItem" id="{id}"><strong>{title}</strong></div></tpl>',
	            itemSelector: '.menuItem',
	            store: this.store,
				scroll: false,
				listeners: {
					scope: this,
					itemtap: function(subList, subIdx, el, e){
						var store  = subList.getStore(),
            				record = store.getAt(subIdx);
							
						//console.log(record.get('title'))
						this.callback(null, record.data);
						//console.log('t', this);
					}
				}
	        });
			this.items = [this.list]
			
			_self.superclass.initComponent.call(this);
		},
		scroll: {
			vertical: true
		}
		
	});
})();

Ext.regModel('StopList', {
    fields: [
        { name: 'title',      type: 'string' },
		{ name: 'sid',        type: 'string' },
    ]
});
