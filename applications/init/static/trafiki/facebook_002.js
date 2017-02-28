FacebookView = (function(){
	var _self;
	return _self = Ext.extend(View, {
		scroll: false,
		title: 'Facebook',
		initComponent: function(){
			this.rightNavButton = new Ext.Button({
	            text: 'Connect',
				ui: 'action'
	        });
			
			this.store = new Ext.data.Store({
				model: 'StopList',
				getGroupString : function(record) { return 'Facebook friends'; },
				data: this.data || [
					{firstName: 'Kate', lastName: 'Leopold'},
                    {firstName: 'Jay', lastName: 'Smith'},
                    {firstName: 'Connor', lastName: 'McDouglas'},
                    {firstName: 'Bill', lastName: 'Oates'},
                    {firstName: 'George', lastName: 'Wellington'},
                    {firstName: 'Tommy', lastName: 'Smith'},
                    {firstName: 'Abraham', lastName: 'Edison'},
                    {firstName: 'Thomas', lastName: 'Robinson'},
				]
			});
			
			this.list = new Ext.List({
				cls: 'facebook',
	            tpl: '<tpl for="."><div class="facebookFriend"><div class="leftImage"><img class="icon team" /></div><strong>{lastName}</strong>, {firstName}</div></tpl>',
	            itemSelector: '.facebookFriend',
	            store: this.store,
				grouped: true,
				listeners: {
					scope: this,
					itemtap: function(subList, subIdx, el, e){
						var store  = subList.getStore(),
            				record = store.getAt(subIdx);
						
						this.callback(null, { title: record.get('firstName')});
					}
				}
	        });
			
			this.items = [this.list]
			_self.superclass.initComponent.call(this);
		}
		
		
	});
})();

Ext.regModel('IconButton', {
    fields: [
        { name: 'title',      type: 'string' },
		{ name: 'sid',        type: 'string' },
    ]
});
