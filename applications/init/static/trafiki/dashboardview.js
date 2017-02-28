DashboardView = (function(){
	var _self;
	return _self = Ext.extend(Ext.Panel, {
		delay: 400,
		editable: true,
		cls: 'dashboardview',
		initComponent: function(){


			this.actions = new Ext.ActionSheet({
			    items: [{
			        text : 'Save',
					ui: 'confirm',
			        handler : Ext.emptyFn
			    },{
			        text : 'Cancel',
					scope: this,
			        handler : function(){ this.toggleEdit(false); }
			    }],
			    modal: false
			});
			
			this.items = this.widgets.map(function(o, i){
				return new window[o.type || "Widget"]({
					o: o
				});
			});
			
			_self.superclass.initComponent.call(this);
		},
		
		afterRender: function(){
			if (this.editable) {
				this.el.on('taphold', function(e){ this.toggleEdit(true, e); }, this, {
					holdThreshold: this.delay
				});
				
				this.sortable = new Ext.util.Sortable(this.el, {
					itemSelector: '.widget',
					direction: 'both',
					scroll: false,
					constrain: true,
					disabled: true
				});
			}
			
			_self.superclass.afterRender.call(this);
		},
		
		initEvents: function(){
			var me = this;
			_self.superclass.initEvents.call(this);
			me.mon(me.el, {
	            scope: me,
				tap: me.onTap
	        });
		},
		
		getWidgetFromPoint: function(e){
			var tmp = e.changedTouches[0];
			return (tmp = Ext.fly(document.elementFromPoint(tmp.pageX, tmp.pageY)).findParent('.widget')) && tmp.id && Ext.getCmp(tmp.id);
		},
		
		onTap: function(e){
			if (!this.sortable || this.sortable.disabled) {
				var widget = this.getWidgetFromPoint(e);
				if (widget) {
					//console.log('tapwidget', widget, 'this', this);
					if (this.onTapCallback) {
						this.onTapCallback(widget);
					}
					else {
						widget.onTap();
					}
				}
			}
		},
		
		sorting: false,
		toggleEdit: function(on, e, a, b, c){
			
			if(on){
				if (this.sortable.disabled) {
					this.el.addClass('editing');
					this.sortable.enable();
					this.sortable.onTapEvent(e, e.target);
					this.actions.show();
				}
			} else {
				this.el.removeClass('editing');
				this.sortable.disable();
				this.actions.hide();
			}
			
		},
		
		
	});
})();