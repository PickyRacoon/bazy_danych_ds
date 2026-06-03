ALTER SESSION SET CURRENT_SCHEMA = US_SPAT;

SELECT p.name, p.geom
FROM us_parks p, us_states s
WHERE s.state = 'Wyoming'
      AND SDO_INSIDE (p.geom, s.geom ) = 'TRUE';
      
SELECT pp.name, pp.geom FROM us_parks pp
WHERE id IN
(
 SELECT p.id
 FROM us_parks p, us_states s
 WHERE s.state = 'Wyoming'
 and SDO_INSIDE (p.geom, s.geom ) = 'TRUE'
);

SELECT state, geom FROM us_states
WHERE state = 'Wyoming';

SELECT p.name, p.geom
FROM us_parks p, us_states s
WHERE s.state = 'Wyoming'
AND SDO_ANYINTERACT (p.geom, s.geom ) = 'TRUE';


      
SELECT pp.name, pp.geom FROM us_parks pp
WHERE id IN
(
 SELECT p.id
 FROM us_parks p, us_states s
 WHERE s.state = 'Wyoming'
 and SDO_ANYINTERACT (p.geom, s.geom ) = 'TRUE'
);
