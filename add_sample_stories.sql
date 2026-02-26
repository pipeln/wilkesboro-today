-- Insert sample stories into news_raw for testing

INSERT INTO news_raw (
    Title_Original,
    Summary_Short,
    Body_Original,
    Category,
    Source_Name,
    Source_URL,
    Status,
    approval_status,
    telegram_notified,
    Date_Original
) VALUES 
(
    'Wilkes County Receives $2M Grant for Broadband Expansion',
    'Federal grant will bring high-speed internet to rural areas of Wilkes County over the next 18 months.',
    'Wilkes County has been awarded a $2 million federal grant to expand broadband internet access to underserved rural areas. The project, funded through the USDA Rural Development program, will install fiber optic infrastructure in areas currently lacking reliable high-speed internet.

County Manager John Smith announced the grant at Tuesday''s Board of Commissioners meeting. "This is a game-changer for our rural residents and businesses," Smith said. "High-speed internet is no longer a luxury—it''s essential for education, healthcare, and economic development."

The project will prioritize areas with the lowest current internet speeds, particularly in the northern and western parts of the county. Installation is expected to begin in June 2026 and be completed by December 2027.

Residents can check their address on the county website to see if they''re in the expansion zone.',
    'Government',
    'Journal Patriot',
    'https://www.journalpatriot.com',
    'New',
    'pending',
    false,
    '2026-02-26'
),
(
    'Local Teen Wins State Wrestling Championship',
    'Wilkes Central High School senior captures 3A state title, first for school in 15 years.',
    'Wilkes Central High School senior Marcus Johnson brought home the 3A state wrestling championship Saturday, becoming the first Warrior to win a state title in 15 years.

Johnson, who competes in the 152-pound weight class, defeated defending champion Tyler Reed of West Henderson High in a dramatic 3-2 decision. The match went to overtime after being tied 2-2 through regulation.

"I''ve been working for this since freshman year," Johnson said. "To finally get it done feels amazing."

Johnson finishes his high school career with a 148-12 record and will wrestle next year at Appalachian State University.',
    'Sports',
    'Wilkes Record',
    'https://www.thewilkesrecord.com',
    'New',
    'pending',
    false,
    '2026-02-25'
),
(
    'New Restaurant Opening Downtown Wilkesboro',
    'Farm-to-table concept ''The Local Plate'' set to open March 15 on Main Street.',
    'A new farm-to-table restaurant is coming to downtown Wilkesboro next month. The Local Plate, located at 123 Main Street, will feature seasonal menus using ingredients from local farms within 50 miles.

Owner Sarah Martinez, a Wilkes County native who trained at Johnson & Wales University, said she wants to showcase the region''s agricultural heritage. "We have amazing farmers here, and I want to put their products front and center," Martinez said.

The restaurant will serve lunch and dinner Tuesday through Saturday, with brunch on Sundays. Reservations open March 1.',
    'Business',
    'Journal Patriot',
    'https://www.journalpatriot.com',
    'New',
    'pending',
    false,
    '2026-02-24'
),
(
    'Brushy Mountain Ruritan Club Announces Scholarship Winners',
    'Five local students receive $1,000 scholarships for college.',
    'The Brushy Mountain Ruritan Club has awarded $5,000 in scholarships to five Wilkes County high school seniors. The scholarships, each worth $1,000, were presented at the club''s monthly meeting Thursday.

Recipients are:
- Emma Thompson (Wilkes Central High)
- James Wilson (West Wilkes High)
- Maria Garcia (East Wilkes High)
- David Brown (Wilkes Early College)
- Lisa Chen (Homeschool)

The scholarships are awarded based on academic achievement, community service, and essays about the importance of rural communities.',
    'Community',
    'Brushy Mountain Ruritan',
    'https://www.brushymountainruritan.org',
    'New',
    'pending',
    false,
    '2026-02-23'
),
(
    'Yadkin River Greenway Reopens After Helene Repairs',
    'Popular walking trail fully restored with $763K in county-funded repairs.',
    'The Yadkin River Greenway has officially reopened after months of repairs following damage from Hurricane Helene. The $763,675 restoration project, funded by Wilkes County, repaired washed-out sections, replaced damaged boardwalks, and improved drainage systems.

"The greenway is one of our community''s most treasured amenities," said Parks Director Mike Johnson. "We know residents have been eager to get back out there."

The 2.5-mile paved trail runs along the Yadkin River from Wilkesboro to North Wilkesboro. New features include improved lighting, additional benches, and emergency call boxes.

The greenway is open daily from dawn to dusk.',
    'Community',
    'Wilkes County Gov',
    'https://www.wilkescounty.net',
    'New',
    'pending',
    false,
    '2026-02-22'
);
