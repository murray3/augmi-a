TimeBar = (function(){
	var _self;
	return _self = Ext.extend(Ext.Toolbar, {
		ui: 'dark',
        dock: 'bottom',
        title: this.title || "",
		initComponent: function(){
			
			this.timeToggle = new Ext.Button({
				ui: 'action',
				cls: 'icon-button',
				iconMask: true,
				iconCls: 'arrive_at',
				arrive: true,
				listeners: {
					afterrender: function(){ this.iconEl = Ext.get(this.el.query('img')[0]); }
				},
				handler: function(){
					this.arrive = !this.arrive;
					this.iconEl
						.removeClass(!this.arrive ? 'arrive_at' : 'leave_at')
						.addClass(this.arrive ? 'arrive_at' : 'leave_at')
				}
			});
			
			this.dateButton = new DragButton({
				date: new Date(),
				text: 'date',
				listeners: {
					stepstart: function(){ this.stepStartDate = new Date(this.date); },
					step: function(step){ var tmp = new Date(this.stepStartDate); tmp.setDate(tmp.getDate() + step); this.date = tmp; this.refresh(); },
					stepend: Ext.emptyFn,
					render: function(cmp){ 
						this.refresh(); 
					}
				},
				refresh: function(){ 
					var str = this.date.format('y-m-d');
					this.setText(str);
					if(this.helpPanel && this.helpPanel.body && !this.helpPanel.hidden){
						this.helpPanel.body.setHTML(str);
					} 
				},
				handler: function(){
					this.dp = new Ext.DatePicker({
						buttonBar: { dock: 'top', title: 'Pick date' },
						yearFrom: this.date.getFullYear(),
						yearTo: this.date.getFullYear() + 1,
						value: this.date,
						listeners: {
							scope: this,
							change: function(picker, value){ this.date = value; this.refresh(); }
						}
					});
					this.dp.show();
				}
			});
			
			this.timeButton = new DragButton({
				date: new Date(),
				text: 'date',
				listeners: {
					stepstart: function(){ this.stepStartDate = new Date(this.date); },
					step: function(step){ var tmp = new Date(this.stepStartDate); tmp.setMinutes(Math.round(tmp.getMinutes() / 10)*10 + step * 10); this.date = tmp; this.refresh(); },
					stepend: Ext.emptyFn,
					render: function(cmp){ 
						this.refresh();
					}
				},
				refresh: function(){  
				    var str = this.date.format('H:i');
					this.setText(str);
					if(this.helpPanel && this.helpPanel.body && !this.helpPanel.hidden){
						this.helpPanel.body.setHTML(str);
					} 
				},
				handler: function(){
					//console.log('this', this, this.date)
					this.tp = new TimePicker({
						buttonBar: { dock: 'top', title: 'Pick time' },
						value: this.date,
						listeners: {
							scope: this,
							change: function(picker, value){ this.date = value; this.refresh(); }
						}
					}); 
					this.tp.show();
				}
			});
			
			this.mot = new Ext.Button({
				ui: 'action',
				//cls: 'icon-button',
				iconMask: true,
				iconCls: 'bus',
			});
			
			this.items = [this.timeToggle, { xtype: 'spacer' }, this.timeButton, this.dateButton, { xtype: 'spacer' }, this.mot];
			_self.superclass.initComponent.call(this);
		}
	});
})();
