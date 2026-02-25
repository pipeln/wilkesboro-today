/* empty css                                  */
import { c as createComponent, r as renderComponent, a as renderTemplate, m as maybeRenderHead } from '../chunks/astro/server_irxFjrx1.mjs';
import 'kleur/colors';
import 'html-escaper';
import { $ as $$Layout } from '../chunks/Layout_stZzsqQZ.mjs';
export { renderers } from '../renderers.mjs';

const $$Events = createComponent(($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, {}, { "default": ($$result2) => renderTemplate`   ${maybeRenderHead()}<section class="bg-gradient-to-br from-primary to-primary-dark text-white py-12"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"> <h1 class="text-4xl font-bold mb-4">Community Events</h1> <p class="text-xl text-blue-100 max-w-2xl mx-auto">
Stay informed about meetings, festivals, job fairs, and community gatherings in Wilkes County and beyond.
</p> </div> </section>  <section class="bg-accent/10 py-4"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between"> <p class="text-gray-700">Know about an event? Help us keep the community informed.</p> <a href="/submit-event" class="px-4 py-2 bg-accent text-white font-medium rounded-lg hover:bg-accent/90 transition">
Submit Event
</a> </div> </section>  <section class="py-12"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> <div class="grid grid-cols-1 lg:grid-cols-3 gap-8"> <!-- Main Calendar --> <div class="lg:col-span-2"> <div class="bg-white rounded-xl shadow-sm overflow-hidden"> <div class="p-4 border-b border-gray-200 flex items-center justify-between"> <h2 class="text-xl font-bold text-gray-900">Event Calendar</h2> <div class="flex space-x-2"> <a href="https://calendar.google.com/calendar/ical/d3c87bf871e68bb4b47ab71d194de22b441895c846c82a5cb11ebb7355dedb09%40group.calendar.google.com/public/basic.ics" class="text-sm text-primary hover:underline flex items-center" target="_blank"> <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path> </svg>
Subscribe
</a> </div> </div> <!-- Google Calendar Embed --> <iframe src="https://calendar.google.com/calendar/embed?src=d3c87bf871e68bb4b47ab71d194de22b441895c846c82a5cb11ebb7355dedb09%40group.calendar.google.com&ctz=America%2FNew_York&showTitle=0&showNav=1&showDate=1&showPrint=0&showTabs=1&showCalendars=0&showTz=1&mode=MONTH" style="border: 0" width="100%" height="600" frameborder="0" scrolling="no" class="w-full"></iframe> </div> </div> <!-- Sidebar --> <div class="space-y-6"> <!-- Upcoming Events List --> <div class="bg-white rounded-xl shadow-sm p-6"> <h3 class="text-lg font-bold text-gray-900 mb-4">Upcoming Events</h3> <div class="space-y-4"> <!-- Event 1 --> <div class="flex items-start space-x-3 pb-4 border-b border-gray-100"> <div class="flex-shrink-0 w-12 text-center bg-primary text-white rounded-lg py-2"> <div class="text-xs uppercase">Mar</div> <div class="text-xl font-bold">5</div> </div> <div> <h4 class="font-semibold text-gray-900">Board of Commissioners Meeting</h4> <p class="text-sm text-gray-600">5:00 PM • Wilkes County Office Building</p> <span class="inline-block mt-1 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded">Government</span> </div> </div> <!-- Event 2 --> <div class="flex items-start space-x-3 pb-4 border-b border-gray-100"> <div class="flex-shrink-0 w-12 text-center bg-accent text-white rounded-lg py-2"> <div class="text-xs uppercase">Mar</div> <div class="text-xl font-bold">6</div> </div> <div> <h4 class="font-semibold text-gray-900">Food Truck Fridays</h4> <p class="text-sm text-gray-600">5:00 PM • Downtown North Wilkesboro</p> <span class="inline-block mt-1 text-xs bg-orange-100 text-orange-800 px-2 py-0.5 rounded">Food & Fun</span> </div> </div> <!-- Event 3 --> <div class="flex items-start space-x-3"> <div class="flex-shrink-0 w-12 text-center bg-green-500 text-white rounded-lg py-2"> <div class="text-xs uppercase">Jul</div> <div class="text-xl font-bold">18</div> </div> <div> <h4 class="font-semibold text-gray-900">NASCAR Craftsman Truck Series</h4> <p class="text-sm text-gray-600">North Wilkesboro Speedway</p> <span class="inline-block mt-1 text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded">Sports</span> </div> </div> </div> </div> <!-- Categories --> <div class="bg-white rounded-xl shadow-sm p-6"> <h3 class="text-lg font-bold text-gray-900 mb-4">Event Categories</h3> <div class="space-y-2"> <a href="#" class="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition"> <span class="flex items-center"> <span class="w-3 h-3 rounded-full bg-blue-500 mr-3"></span>
Government
</span> <span class="text-sm text-gray-500">12</span> </a> <a href="#" class="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition"> <span class="flex items-center"> <span class="w-3 h-3 rounded-full bg-orange-500 mr-3"></span>
Community
</span> <span class="text-sm text-gray-500">8</span> </a> <a href="#" class="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition"> <span class="flex items-center"> <span class="w-3 h-3 rounded-full bg-green-500 mr-3"></span>
Sports
</span> <span class="text-sm text-gray-500">5</span> </a> <a href="#" class="flex items-center justify-between p-2 rounded-lg hover:bg-gray-50 transition"> <span class="flex items-center"> <span class="w-3 h-3 rounded-full bg-purple-500 mr-3"></span>
Schools
</span> <span class="text-sm text-gray-500">6</span> </a> </div> </div> <!-- Add to Your Calendar --> <div class="bg-gradient-to-br from-primary to-primary-dark rounded-xl p-6 text-white"> <h3 class="text-lg font-bold mb-2">📅 Add to Your Calendar</h3> <p class="text-sm text-blue-100 mb-4">Never miss an event. Subscribe to our community calendar.</p> <a href="https://calendar.google.com/calendar/u/0?cid=d3c87bf871e68bb4b47ab71d194de22b441895c846c82a5cb11ebb7355dedb09%40group.calendar.google.com" target="_blank" class="block w-full text-center px-4 py-2 bg-white text-primary font-medium rounded-lg hover:bg-gray-100 transition">
Subscribe with Google
</a> <a href="https://calendar.google.com/calendar/ical/d3c87bf871e68bb4b47ab71d194de22b441895c846c82a5cb11ebb7355dedb09%40group.calendar.google.com/public/basic.ics" class="block w-full text-center px-4 py-2 mt-2 bg-white/20 text-white font-medium rounded-lg hover:bg-white/30 transition">
Download iCal File
</a> </div> </div> </div> </div> </section>  <section class="bg-gray-50 py-12"> <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center"> <h2 class="text-2xl font-bold text-gray-900 mb-4">Hosting an event?</h2> <p class="text-gray-600 mb-6">
Submit your community event, meeting, or gathering to be included in our calendar. 
        All events are reviewed before publishing.
</p> <div class="flex flex-col sm:flex-row gap-4 justify-center"> <a href="/submit-event" class="px-6 py-3 bg-primary text-white font-semibold rounded-lg hover:bg-primary-dark transition">
Submit Event
</a> <a href="mailto:events@wilkesborotoday.com" class="px-6 py-3 bg-white text-gray-700 font-semibold rounded-lg border border-gray-300 hover:bg-gray-50 transition">
Contact Event Team
</a> </div> </div> </section> `, "head": ($$result2) => renderTemplate`<fragment> <title>Community Events - Wilkesboro Today</title> <meta name="description" content="Community events, meetings, and happenings in Wilkes County, North Wilkesboro, and surrounding areas."> </fragment>` })} `;
}, "/root/.openclaw/workspace/website-design/src/pages/events.astro", void 0);

const $$file = "/root/.openclaw/workspace/website-design/src/pages/events.astro";
const $$url = "/events";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Events,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
