/* empty css                                  */
import { c as createComponent, m as maybeRenderHead, a as renderTemplate, b as addAttribute, r as renderComponent } from '../chunks/astro/server_irxFjrx1.mjs';
import 'kleur/colors';
import 'html-escaper';
import { $ as $$Layout } from '../chunks/Layout_stZzsqQZ.mjs';
import 'clsx';
export { renderers } from '../renderers.mjs';

const $$WeatherWidget = createComponent(($$result, $$props, $$slots) => {
  const currentWeather = {
    temp: 54,
    condition: "Partly Cloudy",
    high: 58,
    low: 42,
    humidity: 65,
    wind: "8 mph NW",
    forecast: [
      { day: "Wed", high: 58, low: 44, icon: "\u{1F327}\uFE0F", condition: "Rain Likely" },
      { day: "Thu", high: 56, low: 42, icon: "\u{1F327}\uFE0F", condition: "Showers" },
      { day: "Fri", high: 62, low: 38, icon: "\u26C5", condition: "Partly Sunny" },
      { day: "Sat", high: 65, low: 40, icon: "\u2600\uFE0F", condition: "Sunny" },
      { day: "Sun", high: 64, low: 42, icon: "\u2600\uFE0F", condition: "Clear" }
    ]
  };
  return renderTemplate`${maybeRenderHead()}<div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg"> <div class="flex items-center justify-between mb-4"> <div> <p class="text-blue-100 text-sm">Wilkesboro, NC</p> <p class="text-3xl font-bold">${currentWeather.temp}°F</p> <p class="text-blue-100">${currentWeather.condition}</p> </div> <div class="text-6xl">⛅</div> </div> <div class="grid grid-cols-3 gap-4 text-center text-sm mb-6"> <div class="bg-white/10 rounded-lg p-2"> <p class="text-blue-200">High/Low</p> <p class="font-semibold">${currentWeather.high}°/${currentWeather.low}°</p> </div> <div class="bg-white/10 rounded-lg p-2"> <p class="text-blue-200">Humidity</p> <p class="font-semibold">${currentWeather.humidity}%</p> </div> <div class="bg-white/10 rounded-lg p-2"> <p class="text-blue-200">Wind</p> <p class="font-semibold">${currentWeather.wind}</p> </div> </div> <div class="border-t border-white/20 pt-4"> <p class="text-sm font-semibold mb-3">5-Day Forecast</p> <div class="grid grid-cols-5 gap-2 text-center"> ${currentWeather.forecast.map((day) => renderTemplate`<div class="bg-white/10 rounded-lg p-2"> <p class="text-xs text-blue-200">${day.day}</p> <p class="text-xl my-1">${day.icon}</p> <p class="text-xs font-semibold">${day.high}°/${day.low}°</p> </div>`)} </div> </div> <a href="https://weather.gov/gsp" target="_blank" rel="noopener" class="block text-center text-xs text-blue-200 mt-4 hover:text-white">
Data from NWS Greenville-Spartanburg →
</a> </div>`;
}, "/root/.openclaw/workspace/website-design/src/components/WeatherWidget.astro", void 0);

const $$JobsBoard = createComponent(($$result, $$props, $$slots) => {
  const jobs = [
    {
      id: 1,
      title: "Registered Nurse - Wilkes Medical Center",
      company: "Wilkes Medical Center",
      location: "North Wilkesboro, NC",
      type: "Full-time",
      salary: "$28-42/hour",
      posted: "2 days ago",
      category: "Healthcare",
      url: "#"
    },
    {
      id: 2,
      title: "Production Supervisor",
      company: "Tyson Foods",
      location: "Wilkesboro, NC",
      type: "Full-time",
      salary: "$55,000-65,000/year",
      posted: "3 days ago",
      category: "Manufacturing",
      url: "#"
    },
    {
      id: 3,
      title: "Store Manager",
      company: "Lowe's",
      location: "Wilkesboro, NC",
      type: "Full-time",
      salary: "$50,000-70,000/year",
      posted: "1 week ago",
      category: "Retail",
      url: "#"
    },
    {
      id: 4,
      title: "CDL Truck Driver",
      company: "Old Dominion Freight Line",
      location: "Wilkes County, NC",
      type: "Full-time",
      salary: "$65,000-80,000/year",
      posted: "4 days ago",
      category: "Transportation",
      url: "#"
    },
    {
      id: 5,
      title: "Teacher - Elementary",
      company: "Wilkes County Schools",
      location: "Wilkes County, NC",
      type: "Full-time",
      salary: "$37,000-52,000/year",
      posted: "1 week ago",
      category: "Education",
      url: "#"
    }
  ];
  const categories = ["All", "Healthcare", "Manufacturing", "Retail", "Education", "Transportation", "Government"];
  return renderTemplate`${maybeRenderHead()}<section class="bg-white rounded-xl shadow-sm p-6"> <div class="flex items-center justify-between mb-6"> <h2 class="text-xl font-bold text-gray-900 flex items-center"> <span class="w-1 h-6 bg-green-500 mr-3 rounded"></span>
Jobs in Wilkes County
</h2> <a href="https://www.ncworks.gov" target="_blank" rel="noopener" class="text-primary text-sm hover:underline">
View on NCWorks →
</a> </div> <!-- Category Filter --> <div class="flex flex-wrap gap-2 mb-6"> ${categories.map((cat, i) => renderTemplate`<button${addAttribute(`px-3 py-1 rounded-full text-sm font-medium transition ${i === 0 ? "bg-green-500 text-white" : "bg-gray-100 text-gray-700 hover:bg-gray-200"}`, "class")}> ${cat} </button>`)} </div> <!-- Job Listings --> <div class="space-y-4"> ${jobs.map((job) => renderTemplate`<a${addAttribute(job.url, "href")} class="block border border-gray-200 rounded-lg p-4 hover:border-green-500 hover:shadow-sm transition group"> <div class="flex items-start justify-between"> <div class="flex-1"> <div class="flex items-center gap-2 mb-1"> <span class="text-xs font-semibold text-green-600 bg-green-50 px-2 py-0.5 rounded"> ${job.category} </span> <span class="text-xs text-gray-500">${job.posted}</span> </div> <h3 class="font-semibold text-gray-900 group-hover:text-green-600 transition"> ${job.title} </h3> <p class="text-sm text-gray-600">${job.company}</p> <div class="flex items-center gap-4 mt-2 text-sm text-gray-500"> <span class="flex items-center"> <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path> </svg> ${job.location} </span> <span class="flex items-center"> <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path> </svg> ${job.type} </span> </div> </div> <div class="text-right"> <p class="font-semibold text-gray-900">${job.salary}</p> <span class="text-green-600 text-sm">Apply →</span> </div> </div> </a>`)} </div> <!-- Submit Job CTA --> <div class="mt-6 p-4 bg-gray-50 rounded-lg text-center"> <p class="text-sm text-gray-600 mb-2">Are you hiring? Post your job opening.</p> <a href="/submit-job" class="inline-block px-4 py-2 bg-green-500 text-white text-sm font-medium rounded-lg hover:bg-green-600 transition">
Post a Job
</a> </div> </section>`;
}, "/root/.openclaw/workspace/website-design/src/components/JobsBoard.astro", void 0);

const $$AreaNewsFeed = createComponent(($$result, $$props, $$slots) => {
  const localNews = [
    {
      id: 1,
      title: "Wilkes County Schools Superintendent Mark Byrd passes away",
      source: "Journal Patriot",
      time: "2 hours ago",
      category: "Breaking",
      url: "#"
    },
    {
      id: 2,
      title: "County Commissioners meeting rescheduled to March 5",
      source: "Wilkes County Gov",
      time: "4 hours ago",
      category: "Government",
      url: "#"
    },
    {
      id: 3,
      title: "Food Truck Fridays returning to downtown North Wilkesboro",
      source: "Town of N. Wilkesboro",
      time: "6 hours ago",
      category: "Events",
      url: "#"
    }
  ];
  const stateNews = [
    {
      id: 1,
      title: "NC Legislature considers new education funding bill",
      source: "WRAL",
      time: "1 hour ago",
      category: "Politics",
      url: "#"
    },
    {
      id: 2,
      title: "State health officials report flu cases declining",
      source: "NC DHHS",
      time: "3 hours ago",
      category: "Health",
      url: "#"
    },
    {
      id: 3,
      title: "New highway expansion project announced for I-40",
      source: "NCDOT",
      time: "5 hours ago",
      category: "Transportation",
      url: "#"
    }
  ];
  const nearbyNews = [
    {
      id: 1,
      title: "Boone approves new affordable housing development",
      source: "Watauga Democrat",
      location: "Boone",
      time: "2 hours ago",
      url: "#"
    },
    {
      id: 2,
      title: "Asheville tourism rebounds post-Helene",
      source: "Mountain Xpress",
      location: "Asheville",
      time: "4 hours ago",
      url: "#"
    },
    {
      id: 3,
      title: "Winston-Salem opens new business incubator",
      source: "Winston-Salem Journal",
      location: "Winston-Salem",
      time: "6 hours ago",
      url: "#"
    }
  ];
  return renderTemplate`${maybeRenderHead()}<section class="space-y-6"> <!-- Tabs --> <div class="flex space-x-1 bg-gray-100 p-1 rounded-lg"> <button class="flex-1 py-2 px-4 rounded-md bg-white text-primary font-medium shadow-sm">
Local
</button> <button class="flex-1 py-2 px-4 rounded-md text-gray-600 hover:text-gray-900">
State
</button> <button class="flex-1 py-2 px-4 rounded-md text-gray-600 hover:text-gray-900">
Nearby
</button> </div> <!-- Local News --> <div class="bg-white rounded-xl shadow-sm p-6"> <div class="flex items-center justify-between mb-4"> <h3 class="text-lg font-bold text-gray-900">Wilkes County</h3> <span class="text-xs text-gray-500">Live updates</span> </div> <div class="space-y-4"> ${localNews.map((item) => renderTemplate`<a${addAttribute(item.url, "href")} class="block group"> <div class="flex items-start space-x-3"> <span${addAttribute(`flex-shrink-0 w-2 h-2 mt-2 rounded-full ${item.category === "Breaking" ? "bg-red-500 animate-pulse" : "bg-primary"}`, "class")}></span> <div class="flex-1"> <h4 class="font-medium text-gray-900 group-hover:text-primary transition line-clamp-2"> ${item.title} </h4> <div class="flex items-center text-xs text-gray-500 mt-1"> <span class="font-medium text-gray-600">${item.source}</span> <span class="mx-1">•</span> <span>${item.time}</span> ${item.category === "Breaking" && renderTemplate`<span class="ml-2 text-red-600 font-medium">BREAKING</span>`} </div> </div> </div> </a>`)} </div> <a href="/news/local" class="block text-center text-primary text-sm hover:underline mt-4">
More local news →
</a> </div> <!-- State News --> <div class="bg-white rounded-xl shadow-sm p-6"> <div class="flex items-center justify-between mb-4"> <h3 class="text-lg font-bold text-gray-900">North Carolina</h3> <span class="text-xs text-gray-500">Statewide</span> </div> <div class="space-y-4"> ${stateNews.map((item) => renderTemplate`<a${addAttribute(item.url, "href")} class="block group"> <div class="flex items-start space-x-3"> <span class="flex-shrink-0 w-2 h-2 mt-2 rounded-full bg-blue-500"></span> <div class="flex-1"> <h4 class="font-medium text-gray-900 group-hover:text-primary transition line-clamp-2"> ${item.title} </h4> <div class="flex items-center text-xs text-gray-500 mt-1"> <span class="font-medium text-gray-600">${item.source}</span> <span class="mx-1">•</span> <span>${item.time}</span> </div> </div> </div> </a>`)} </div> <a href="/news/state" class="block text-center text-primary text-sm hover:underline mt-4">
More state news →
</a> </div> <!-- Nearby Areas --> <div class="bg-white rounded-xl shadow-sm p-6"> <div class="flex items-center justify-between mb-4"> <h3 class="text-lg font-bold text-gray-900">Nearby Areas</h3> <span class="text-xs text-gray-500">WNC Region</span> </div> <div class="space-y-4"> ${nearbyNews.map((item) => renderTemplate`<a${addAttribute(item.url, "href")} class="block group"> <div class="flex items-start space-x-3"> <span class="flex-shrink-0 w-2 h-2 mt-2 rounded-full bg-green-500"></span> <div class="flex-1"> <h4 class="font-medium text-gray-900 group-hover:text-primary transition line-clamp-2"> ${item.title} </h4> <div class="flex items-center text-xs text-gray-500 mt-1"> <span class="font-medium text-gray-600">${item.source}</span> <span class="mx-1">•</span> <span class="text-green-600">${item.location}</span> <span class="mx-1">•</span> <span>${item.time}</span> </div> </div> </div> </a>`)} </div> <a href="/news/regional" class="block text-center text-primary text-sm hover:underline mt-4">
More regional news →
</a> </div> </section>`;
}, "/root/.openclaw/workspace/website-design/src/components/AreaNewsFeed.astro", void 0);

const $$FeedsDirectory = createComponent(($$result, $$props, $$slots) => {
  const feedCategories = [
    {
      name: "Local News",
      icon: "\u{1F4F0}",
      feeds: [
        { name: "Wilkes Journal-Patriot", url: "https://www.journalpatriot.com/rss", status: "active" },
        { name: "Wilkes Record", url: "https://www.thewilkesrecord.com/rss", status: "active" },
        { name: "WXII 12 Wilkes", url: "https://www.wxii12.com/wilkes-county/rss", status: "limited" }
      ]
    },
    {
      name: "Government",
      icon: "\u{1F3DB}\uFE0F",
      feeds: [
        { name: "Wilkes County", url: "https://www.wilkescounty.net/RSSFeed.aspx", status: "active" },
        { name: "North Wilkesboro", url: "https://www.north-wilkesboro.com/rss.aspx", status: "active" },
        { name: "NC Legislature", url: "https://www.ncleg.gov/rss", status: "active" }
      ]
    },
    {
      name: "Regional",
      icon: "\u{1F3D4}\uFE0F",
      feeds: [
        { name: "Mountain Xpress", url: "https://mountainx.com/feed/", status: "active" },
        { name: "Watauga Democrat", url: "https://www.wataugademocrat.com/rss", status: "active" },
        { name: "Buncombe County", url: "https://www.buncombenc.gov/rss.aspx", status: "active" }
      ]
    },
    {
      name: "State News",
      icon: "\u{1F31F}",
      feeds: [
        { name: "WRAL", url: "https://www.wral.com/rss", status: "active" },
        { name: "ABC11", url: "https://abc11.com/rss", status: "active" },
        { name: "WFMY News 2", url: "https://www.wfmynews2.com/rss", status: "active" }
      ]
    },
    {
      name: "Weather",
      icon: "\u{1F324}\uFE0F",
      feeds: [
        { name: "NWS Greenville-Spartanburg", url: "https://www.weather.gov/gsp/", status: "active" },
        { name: "NWS Raleigh", url: "https://www.weather.gov/rah/", status: "active" },
        { name: "NWS National RSS", url: "https://www.weather.gov/rss/", status: "active" }
      ]
    },
    {
      name: "Education",
      icon: "\u{1F393}",
      feeds: [
        { name: "Appalachian State", url: "https://news.appstate.edu/rss", status: "pending" },
        { name: "Wilkes County Schools", url: "#", status: "pending" }
      ]
    }
  ];
  return renderTemplate`${maybeRenderHead()}<section class="bg-white rounded-xl shadow-sm p-6"> <div class="flex items-center justify-between mb-6"> <h2 class="text-xl font-bold text-gray-900 flex items-center"> <span class="w-1 h-6 bg-purple-500 mr-3 rounded"></span>
RSS Feed Directory
</h2> <a href="/feeds.opml" class="text-sm text-primary hover:underline">
Download OPML →
</a> </div> <div class="grid grid-cols-1 md:grid-cols-2 gap-4"> ${feedCategories.map((category) => renderTemplate`<div class="border border-gray-200 rounded-lg p-4"> <div class="flex items-center mb-3"> <span class="text-2xl mr-2">${category.icon}</span> <h3 class="font-semibold text-gray-900">${category.name}</h3> </div> <ul class="space-y-2"> ${category.feeds.map((feed) => renderTemplate`<li class="flex items-center justify-between"> <div class="flex items-center"> <span${addAttribute(`w-2 h-2 rounded-full mr-2 ${feed.status === "active" ? "bg-green-500" : feed.status === "limited" ? "bg-yellow-500" : "bg-gray-300"}`, "class")}></span> <span class="text-sm text-gray-700">${feed.name}</span> </div> <a${addAttribute(feed.url, "href")} target="_blank" rel="noopener" class="text-xs text-gray-400 hover:text-primary" title="View RSS Feed">
RSS
</a> </li>`)} </ul> </div>`)} </div> <div class="mt-6 p-4 bg-gray-50 rounded-lg"> <h4 class="font-semibold text-gray-900 mb-2">📡 About Our Feeds</h4> <p class="text-sm text-gray-600 mb-3">
We aggregate news from 20+ local and regional sources. Our system checks for updates every 2 hours. 
      You can subscribe to any of these feeds in your favorite RSS reader.
</p> <div class="flex items-center gap-4 text-xs"> <span class="flex items-center"> <span class="w-2 h-2 rounded-full bg-green-500 mr-1"></span> Active
</span> <span class="flex items-center"> <span class="w-2 h-2 rounded-full bg-yellow-500 mr-1"></span> Limited
</span> <span class="flex items-center"> <span class="w-2 h-2 rounded-full bg-gray-300 mr-1"></span> Pending
</span> </div> </div> </section>`;
}, "/root/.openclaw/workspace/website-design/src/components/FeedsDirectory.astro", void 0);

const $$ResourcesByCounty = createComponent(($$result, $$props, $$slots) => {
  const counties = [
    {
      name: "Wilkes County",
      slug: "wilkes",
      resources: [
        { category: "Housing", items: [
          { name: "Catherine H. Barber Memorial Shelter", phone: "336-838-7120", address: "3200 Statesville Rd N, North Wilkesboro" },
          { name: "Wilkes Housing Authority", phone: "336-667-8979", address: "Wilkesboro, NC" },
          { name: "Wilkes County DSS", phone: "336-651-7400", address: "PO Box 119, Wilkesboro" }
        ] },
        { category: "Food", items: [
          { name: "Samaritan Kitchen of Wilkes", phone: "", address: "Wilkesboro", note: "Evening meals 5pm" },
          { name: "Meals on Wheels", phone: "", address: "Wilkes County", note: "Home delivery for seniors" },
          { name: "SKYWATCH Food Pantry", phone: "336-838-1965", address: "North Wilkesboro" }
        ] },
        { category: "Jobs", items: [
          { name: "NCWorks Career Center", phone: "336-651-7400", address: "Wilkesboro" },
          { name: "Goodwill Career Connections", phone: "", address: "1821 US Hwy 421, Wilkesboro" }
        ] },
        { category: "Health", items: [
          { name: "Wilkes Health Department", phone: "336-651-7450", address: "306 College St, Wilkesboro" },
          { name: "Care Connection", phone: "336-667-2273", address: "Wilkes County" }
        ] }
      ]
    },
    {
      name: "Watauga County",
      slug: "watauga",
      resources: [
        { category: "Housing", items: [
          { name: "Hospitality House", phone: "828-264-1237", address: "Boone, NC" },
          { name: "Watauga Housing Authority", phone: "828-264-6378", address: "Boone, NC" }
        ] },
        { category: "Food", items: [
          { name: "Hunger Coalition", phone: "828-262-1628", address: "Boone, NC" },
          { name: "ASU Food Pantry", phone: "", address: "Appalachian State University" }
        ] },
        { category: "Jobs", items: [
          { name: "NCWorks Boone", phone: "828-265-5375", address: "Boone, NC" }
        ] }
      ]
    },
    {
      name: "Ashe County",
      slug: "ashe",
      resources: [
        { category: "Housing", items: [
          { name: "Ashe Shelter", phone: "336-846-4357", address: "Jefferson, NC" }
        ] },
        { category: "Food", items: [
          { name: "Ashe Outreach", phone: "336-982-4587", address: "West Jefferson, NC" }
        ] }
      ]
    },
    {
      name: "Alleghany County",
      slug: "alleghany",
      resources: [
        { category: "Housing", items: [
          { name: "Alleghany Housing Authority", phone: "336-372-4455", address: "Sparta, NC" }
        ] },
        { category: "Food", items: [
          { name: "Sparta Food Pantry", phone: "336-372-8663", address: "Sparta, NC" }
        ] }
      ]
    },
    {
      name: "Caldwell County",
      slug: "caldwell",
      resources: [
        { category: "Housing", items: [
          { name: "Caldwell Housing Authority", phone: "828-754-9705", address: "Lenoir, NC" }
        ] },
        { category: "Jobs", items: [
          { name: "NCWorks Lenoir", phone: "828-726-5625", address: "Lenoir, NC" }
        ] }
      ]
    },
    {
      name: "Surry County",
      slug: "surry",
      resources: [
        { category: "Housing", items: [
          { name: "Surry Housing Authority", phone: "336-786-6141", address: "Mount Airy, NC" }
        ] },
        { category: "Jobs", items: [
          { name: "NCWorks Mount Airy", phone: "336-786-4162", address: "Mount Airy, NC" }
        ] }
      ]
    }
  ];
  const categories = ["All", "Housing", "Food", "Jobs", "Health", "Emergency"];
  return renderTemplate`${maybeRenderHead()}<section class="space-y-6"> <!-- Filters --> <div class="bg-white rounded-xl shadow-sm p-4"> <div class="flex flex-wrap gap-2 mb-4"> <span class="text-sm font-medium text-gray-700 mr-2">Category:</span> ${categories.map((cat, i) => renderTemplate`<button${addAttribute(`px-3 py-1 rounded-full text-sm font-medium transition ${i === 0 ? "bg-primary text-white" : "bg-gray-100 text-gray-700 hover:bg-gray-200"}`, "class")}> ${cat} </button>`)} </div> <div class="flex flex-wrap gap-2"> <span class="text-sm font-medium text-gray-700 mr-2">County:</span> <button class="px-3 py-1 rounded-full text-sm font-medium bg-primary text-white">All</button> ${counties.map((county) => renderTemplate`<button class="px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition"> ${county.name} </button>`)} </div> </div> <!-- County Resources --> <div class="space-y-6"> ${counties.map((county) => renderTemplate`<div class="bg-white rounded-xl shadow-sm overflow-hidden"> <div class="bg-gradient-to-r from-primary to-primary-dark px-6 py-4"> <h3 class="text-lg font-bold text-white">${county.name}</h3> </div> <div class="p-6"> <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"> ${county.resources.map((resourceCat) => renderTemplate`<div class="border border-gray-200 rounded-lg p-4"> <h4 class="font-semibold text-gray-900 mb-3 flex items-center"> ${resourceCat.category === "Housing" && renderTemplate`<span class="mr-2">🏠</span>`} ${resourceCat.category === "Food" && renderTemplate`<span class="mr-2">🍽️</span>`} ${resourceCat.category === "Jobs" && renderTemplate`<span class="mr-2">💼</span>`} ${resourceCat.category === "Health" && renderTemplate`<span class="mr-2">🏥</span>`} ${resourceCat.category === "Emergency" && renderTemplate`<span class="mr-2">🚨</span>`} ${resourceCat.category} </h4> <ul class="space-y-3"> ${resourceCat.items.map((item) => renderTemplate`<li class="text-sm"> <p class="font-medium text-gray-900">${item.name}</p> ${item.phone && renderTemplate`<a${addAttribute(`tel:${item.phone}`, "href")} class="text-primary hover:underline">
📞 ${item.phone} </a>`} <p class="text-gray-600">${item.address}</p> ${item.note && renderTemplate`<p class="text-gray-500 text-xs mt-1">${item.note}</p>`} </li>`)} </ul> </div>`)} </div> </div> </div>`)} </div> <!-- Submit Resource CTA --> <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white text-center"> <h3 class="text-xl font-bold mb-2">Know a resource we should add?</h3> <p class="mb-4">Help us keep our community resource directory up to date.</p> <a href="/submit-resource" class="inline-block px-6 py-3 bg-white text-green-600 font-semibold rounded-lg hover:bg-gray-100 transition">
Submit a Resource
</a> </div> </section>`;
}, "/root/.openclaw/workspace/website-design/src/components/ResourcesByCounty.astro", void 0);

const AITABLE_CONFIG = {
  baseUrl: "https://api.aitable.ai/fusion/v1",
  token: "uskNPM9fPVHOgAGbDepyKER",
  datasheets: {
    news: "dstjSJ3rvilwBd3Bae",
    events: "dstnnbs9qm9DZJkt8L",
    resources: "dstRRB7Fi8ZVP7eRcS",
    submissions: "dstD2x1pp48NxsMCjs"
  }
};
async function fetchAITableRecords(datasheetId, options = {}) {
  const { maxRecords = 100, view, filterByFormula } = options;
  const params = new URLSearchParams();
  if (maxRecords) params.append("pageSize", maxRecords.toString());
  if (view) params.append("viewId", view);
  const url = `${AITABLE_CONFIG.baseUrl}/datasheets/${datasheetId}/records?${params}`;
  try {
    const response = await fetch(url, {
      headers: {
        "Authorization": `Bearer ${AITABLE_CONFIG.token}`,
        "Content-Type": "application/json"
      }
    });
    if (!response.ok) {
      throw new Error(`AITable API error: ${response.status}`);
    }
    const data = await response.json();
    return data.data?.records || [];
  } catch (error) {
    console.error("Error fetching from AITable:", error);
    return [];
  }
}
async function getNewsArticles(limit = 10) {
  const records = await fetchAITableRecords(AITABLE_CONFIG.datasheets.news, {
    maxRecords: limit
  });
  return records.map((record) => ({
    id: record.recordId,
    title: record.fields.Title_Original || record.fields.Title,
    summary: record.fields.Summary_Short || record.fields.Body_Original?.substring(0, 200),
    body: record.fields.Body_Original,
    category: record.fields.Category,
    source: record.fields.Source_Name,
    sourceUrl: record.fields.Source_URL,
    date: record.fields.Date_Original,
    location: record.fields.Location,
    slug: slugify(record.fields.Title_Original || record.fields.Title)
  }));
}
async function getEvents(limit = 10) {
  const records = await fetchAITableRecords(AITABLE_CONFIG.datasheets.events, {
    maxRecords: limit
  });
  return records.map((record) => ({
    id: record.recordId,
    title: record.fields.Title,
    description: record.fields.Description,
    date: record.fields.Date_Start,
    time: record.fields.Time_Start,
    venue: record.fields.Venue_Name,
    address: record.fields.Venue_Address,
    city: record.fields.City,
    organizer: record.fields.Organizer_Name,
    sourceUrl: record.fields.Source_URL
  }));
}
function slugify(text) {
  return text.toString().toLowerCase().trim().replace(/\s+/g, "-").replace(/[^\w\-]+/g, "").replace(/\-\-+/g, "-");
}

const $$Index = createComponent(async ($$result, $$props, $$slots) => {
  const articles = await getNewsArticles(6);
  const events = await getEvents(5);
  const featuredArticle = articles[0];
  const latestNews = articles.slice(1, 4);
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, {}, { "default": async ($$result2) => renderTemplate`    ${maybeRenderHead()}<section class="bg-gray-50 py-8"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> <div class="grid grid-cols-1 lg:grid-cols-3 gap-8"> <!-- Featured Story --> <div class="lg:col-span-2"> ${featuredArticle ? renderTemplate`<a${addAttribute(`/news/${featuredArticle.slug}`, "href")} class="group block"> <article class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition"> <div class="aspect-video bg-gray-200 relative"> <div class="absolute inset-0 flex items-center justify-center text-gray-400"> <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path> </svg> </div> <span class="absolute top-4 left-4 bg-secondary text-white text-xs font-bold px-3 py-1 rounded-full"> ${featuredArticle.category} </span> </div> <div class="p-6"> <h1 class="text-2xl md:text-3xl font-bold text-gray-900 mb-3 group-hover:text-primary transition"> ${featuredArticle.title} </h1> <p class="text-gray-600 mb-4 line-clamp-3"> ${featuredArticle.summary} </p> <div class="flex items-center text-sm text-gray-500"> <span>${featuredArticle.source}</span> <span class="mx-2">•</span> <span>${new Date(featuredArticle.date).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</span> </div> </div> </article> </a>` : renderTemplate`<div class="bg-white rounded-xl shadow-sm p-12 text-center"> <p class="text-gray-500">Loading featured story...</p> </div>`} </div> <!-- Weather & Top Stories --> <div class="space-y-6"> ${renderComponent($$result2, "WeatherWidget", $$WeatherWidget, {})} <div class="bg-white rounded-xl shadow-sm p-6"> <h2 class="text-lg font-bold text-gray-900 flex items-center mb-4"> <span class="w-1 h-6 bg-primary mr-3 rounded"></span>
Top Stories
</h2> ${latestNews.map((article) => renderTemplate`<a${addAttribute(`/news/${article.slug}`, "href")} class="group block py-3 border-b border-gray-100 last:border-0"> <span class="text-xs font-semibold text-primary uppercase">${article.category}</span> <h3 class="font-medium text-gray-900 group-hover:text-primary transition line-clamp-2"> ${article.title} </h3> <div class="flex items-center text-xs text-gray-500 mt-1"> <span>${article.source}</span> <span class="mx-1">•</span> <span>${new Date(article.date).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</span> </div> </a>`)} <a href="/news" class="block text-center text-primary font-medium hover:underline mt-4">
View All News →
</a> </div> </div> </div> </div> </section>  <section class="py-12"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> <div class="grid grid-cols-1 lg:grid-cols-3 gap-8"> <div class="lg:col-span-2"> ${renderComponent($$result2, "AreaNewsFeed", $$AreaNewsFeed, {})} </div> <div> ${renderComponent($$result2, "JobsBoard", $$JobsBoard, {})} </div> </div> </div> </section>  <section class="bg-gray-50 py-12"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> <div class="flex items-center justify-between mb-8"> <h2 class="text-2xl font-bold text-gray-900 flex items-center"> <span class="w-1 h-8 bg-primary mr-3 rounded"></span>
Latest News
</h2> <div class="flex space-x-2"> <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium">All</button> <button class="px-4 py-2 bg-white text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-100">Local</button> <button class="px-4 py-2 bg-white text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-100">State</button> <button class="px-4 py-2 bg-white text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-100">Regional</button> </div> </div> <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"> ${articles.slice(0, 6).map((article) => renderTemplate`<a${addAttribute(`/news/${article.slug}`, "href")} class="group"> <article class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition h-full flex flex-col"> <div class="aspect-video bg-gray-100 relative"> <div class="absolute inset-0 flex items-center justify-center text-gray-300"> <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path> </svg> </div> <span class="absolute top-3 left-3 bg-primary/90 text-white text-xs font-bold px-2 py-1 rounded"> ${article.category} </span> </div> <div class="p-5 flex-1 flex flex-col"> <h3 class="font-bold text-lg text-gray-900 mb-2 group-hover:text-primary transition line-clamp-2"> ${article.title} </h3> <p class="text-gray-600 text-sm line-clamp-2 mb-4 flex-1"> ${article.summary} </p> <div class="flex items-center justify-between text-xs text-gray-500 pt-4 border-t border-gray-100"> <span>${article.source}</span> <span>${new Date(article.date).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</span> </div> </div> </article> </a>`)} </div> </div> </section>  <section class="py-12"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> <div class="grid grid-cols-1 lg:grid-cols-2 gap-12"> <!-- Upcoming Events --> <div> <h2 class="text-2xl font-bold text-gray-900 flex items-center mb-6"> <span class="w-1 h-8 bg-accent mr-3 rounded"></span>
Upcoming Events
</h2> <div class="space-y-4"> ${events.map((event) => renderTemplate`<div class="bg-white rounded-lg p-4 shadow-sm flex items-start space-x-4"> <div class="flex-shrink-0 w-16 text-center"> <div class="bg-primary text-white rounded-t-lg py-1 text-xs font-bold uppercase"> ${new Date(event.date).toLocaleDateString("en-US", { month: "short" })} </div> <div class="bg-gray-100 rounded-b-lg py-2"> <span class="text-2xl font-bold text-gray-900"> ${new Date(event.date).getDate()} </span> </div> </div> <div class="flex-1"> <h3 class="font-semibold text-gray-900">${event.title}</h3> <p class="text-sm text-gray-600 mt-1">${event.time} • ${event.venue}</p> <p class="text-sm text-gray-500 mt-1">${event.city}</p> </div> </div>`)} </div> <a href="/events" class="block text-center text-primary font-medium hover:underline mt-6">
View All Events →
</a> </div> <!-- RSS Feeds Directory --> <div> ${renderComponent($$result2, "FeedsDirectory", $$FeedsDirectory, {})} </div> </div> </div> </section>  <section class="bg-gray-50 py-12"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"> <h2 class="text-2xl font-bold text-gray-900 flex items-center mb-8"> <span class="w-1 h-8 bg-green-500 mr-3 rounded"></span>
Community Resources by County
</h2> ${renderComponent($$result2, "ResourcesByCounty", $$ResourcesByCounty, {})} </div> </section>  <section class="py-16"> <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center"> <h2 class="text-3xl font-bold text-gray-900 mb-4">Have a news tip or event?</h2> <p class="text-lg text-gray-600 mb-8">
Help keep our community informed. Submit news tips, events, jobs, or resources for publication.
</p> <a href="/submit" class="inline-flex items-center px-8 py-4 bg-primary text-white font-semibold rounded-lg hover:bg-primary-dark transition shadow-lg hover:shadow-xl">
Submit News or Event
<svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path> </svg> </a> </div> </section> `, "head": async ($$result2) => renderTemplate`<fragment> <title>Wilkesboro Today - Local News, Events & Resources for Wilkes County, NC</title> <meta name="description" content="Your trusted source for local news, events, jobs, weather, and community resources in Wilkes County, North Carolina."> </fragment>` })}`;
}, "/root/.openclaw/workspace/website-design/src/pages/index.astro", void 0);

const $$file = "/root/.openclaw/workspace/website-design/src/pages/index.astro";
const $$url = "";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
