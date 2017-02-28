HelpView = (function(){
	var _self;
	return _self = Ext.extend(Ext.Panel, {
		cls: 'info',
		scroll: true,
		title: 'Info',
		initComponent: function(){
			this.html = [
				"<h1>A new take on public transport</h1>",
				"<p>Public transport is not the most glamorous mean of transport, nor should it try to. However, it should be super simple to use, and deliver perfect information in realtime. One way of doing that is through using this radically rethought interface. So, what is it all about?</p>",
				"<p>Earlier, people mostly travelled between a few points, and always in the same order. Nowadays, the number of points have grown, and we travel between them interchangeably. Therefore, the old, linear, travel planning interface is not valid anymore.</p>",
				"<p>Instead of textfields, we have chosen a customizable widget interface. A widget can be a public transport stop, like the train station, or an address, like your home. It can also be a stop finder - like a Facebook widget where you can pick among your friends and we automagically find the best public transport stop close to him or her.</p>",
				"<p>Also - why not take advantage of the touch based hardware of today? If you'd like to go from one point to the other, just slide your finger between them. This means that there is no such thing as strict routes - everything is freeform, meaning insanely powerful.</p>",
				"<p>Please try out the widget interface. Tap a widget to access realtime info about a stop, maps and timetables. Slide between different widgets to plan trips, taphold to sort them, customize their appearance and pick new ones. Also, try the dragbuttons on the bottom - want to quickly change the time just slightly, then just touch and drag horizontally. Another tip - if you're deep down the navigation tree, just taphold the backbutton the return to the widget view. Want a widget for your LinkedIn contacts, your football team or something else? This will be easy pie to hook into the planned open ecosystem.</p>"
			].join("\n");
			this.styleHtmlContent = true;
			
			_self.superclass.initComponent.call(this);
		}
	});
})();
