# **Automotive Requirements for the Infrastructure to Vehicle Information (IVI) Service** 

## **CAR 2 CAR Communication Consortium** 

## **About the C2C-CC** 

Enhancing road safety and traffic efficiency by means of Cooperative Intelligent Transport Systems and Services (C-ITS) is the dedicated goal of the CAR 2 CAR Communication Consortium. The industrial driven, non-commercial association was founded in 2002 by vehicle manufacturers affiliated with the idea of cooperative road traffic based on Vehicle-to-Vehicle Communications (V2V) and supported by Vehicle-to-Infrastructure Communications (V2I). The Consortium members represent worldwide major vehicle manufactures, equipment suppliers and research organisations. 

Over the years, the CAR 2 CAR Communication Consortium has evolved to be one of the key players in preparing the initial deployment of C-ITS in Europe and the subsequent innovation phases. CAR 2 CAR members focus on wireless V2V communication applications based on ITS-G5 and concentrate all efforts on creating standards to ensure the interoperability of cooperative systems, spanning all vehicle classes across borders and brands. As a key contributor, the CAR 2 CAR Communication Consortium and its members work in close cooperation with the European and international standardisation organisations. 

## **Disclaimer** 

The present document has been developed within the CAR 2 CAR Communication Consortium and might be further elaborated within the CAR 2 CAR Communication Consortium. The CAR 2 CAR Communication Consortium and its members accept no liability for any use of this document and other documents from the CAR 2 CAR Communication Consortium for implementation. CAR 2 CAR Communication Consortium documents should be obtained directly from the CAR 2 CAR Communication Consortium. 

Copyright Notification: No part may be reproduced except as authorized by written permission. The copyright and the foregoing restriction extend to reproduction in all media. © 2021, CAR 2 CAR Communication Consortium. 

## **Document information** 

|**Number:**|2080||**Version:**|n.a.|**Date:**|2021-07-23|
|---|---|---|---|---|---|---|
|**Title:**|Automotive Requirements for the Infrastructure to Vehicle<br>Information (IVI) Service|Automotive Requirements for the Infrastructure to Vehicle<br>Information (IVI) Service|||**Document**<br>**Type:**|RS|
|**Release**|1.6.0||||||
|**Release**|Public||||||
|**Status:**|||||||
|**Status:**|Final||||||



**Table 1: Document information** 

## **Changes since last version** 

|**Date**|**Changes**|**Edited by**|
|---|---|---|
|2021-07-23|•<br>Detailing of iviStatus handling<br>•<br>Several improvements of phrasings and<br>figures<br>•<br>Editorial corrections<br>•<br>Renaming of document from:<br>o Automotive Requirements for<br>IVIM<br>to<br>o Automotive Requirements for<br>the Infrastructure to Vehicle<br>Information (IVI) Service|Release<br>Management|
|2021-03-12|No changes|Release<br>Management|
|2020-12-16|Initial release|Release<br>Management|



**Table 2: Changes since last version** 

## **Table of contents** 

|**Table of contents**|**Table of contents**|
|---|---|
|About the C2C-CC .....................................................................................................................................1||
|Disclaimer .................................................................................................................................................1||
|Document information .............................................................................................................................2||
|Changes since last version ........................................................................................................................3||
|Table of contents ......................................................................................................................................4||
|List of tables .............................................................................................................................................5||
|1|Introduction ......................................................................................................................................6|
|2|Scope ................................................................................................................................................7|
|3|Conventions used .............................................................................................................................8|
|4|Definitions ........................................................................................................................................9|
|5|Parameter settings ........................................................................................................................ 10|
|6|General understanding of the IVIM ............................................................................................... 12|
||6.1<br>Purpose of the In-Vehicle Signage use cases......................................................................... 12|
||6.2<br>Purpose of the different containers in IVIM.......................................................................... 12|
||6.2.1<br>Management Container ............................................................................................................... 12|
||6.2.2<br>Geographic Location Container ................................................................................................... 12|
||6.2.3<br>General IVI Container ................................................................................................................... 13|
|7|Requirement specifications ........................................................................................................... 14|
||7.1<br>IVIM Automotive Requirements............................................................................................ 14|
||7.1.1<br>Transmission ................................................................................................................................ 14|
||7.1.2<br>IviStructure .................................................................................................................................. 14|
||7.1.3<br>ManagementContainer ................................................................................................................ 18|
||7.1.4<br>Geographic Location Container ................................................................................................... 22|
||7.1.5<br>MAP Location Container .............................................................................................................. 28|
||7.1.6<br>General IVI Container Part ........................................................................................................... 28|
||7.2<br>Open questions and subjects ................................................................................................ 35|
||7.2.1<br>Usage of zoneHeading ................................................................................................................. 35|
|8|Annex ............................................................................................................................................. 36|
||8.1<br>IVIM mandatory and optional data elements ....................................................................... 36|



## **List of tables** 

|Table 1: Document information .............................................................................................................. 2|Table 1: Document information .............................................................................................................. 2|
|---|---|
|Table 2: Changes since last version ......................................................................................................... 3|Table 2: Changes since last version ......................................................................................................... 3|
|Table 3: Parameter settings RS_ARI_22 ................................................................................................ 10|Table 3: Parameter settings RS_ARI_22 ................................................................................................ 10|



## **1 Introduction** 

## **Other (informational)** 

**RS_ARI_1** 

This document is part of the documentation within the Work Item F0020 ‘Automotive Requirements for IVIM’. It is the main working document containing identified requirements to the IVIM from an automotive perspective. 

It shall serve as an extension to already existing requirements on IVIM in the C-Roads profiles and specifications. 

## **2 Scope** 

## **Other (informational)** 

## **RS_ARI_2** 

The present document provides requirements related to the features of a C-ITS station transmitting IVIM to enable interoperability. The requirements in this document are intended as an addition to existing requirements in [ISO 19321], [TS 103 301] and the C-Roads profile. 

In this document only, highway use cases were considered, use cases on other road types or in urban areas may need different profiling. Apart from that, the requirements in this document are independent of the specific use case and shall therefore apply to all highway use cases of the InVehicle-Signage Service. 

Furthermore, the requirements are focussed on the functional level, specifications on the lower communication levels are out of scope of this document. Also, for the functional level, these requirements don’t claim to be complete. 

In some cases, requirements are written in a way which let the implementation open, for example if they refer to very specific implementations which may depend on specific national regulations. Those requirements have to be further detailed by anybody implementing that requirement. Beside these special requirements all other requirements can be further detailed, too. 

**3 Conventions used Other (informational)** (RS_BSP_152) **RS_ ARI_3** 

Conventions used in this and other C2C-CC specification documents can be found in [C2CCC ConV]. 

## **4 Definitions** 

## **Definition** 

(RS_BSP_193) **RS_ARI_9** 

‘C-ITS time’ or ‘time base’ means the number of elapsed International Atomic Time (TAI) milliseconds since 2004-01-01 00:00:00.000 Coordinated Universal Time (UTC)+0 as defined in [EN 302 636-4-1]. Timestamps as defined in [TS 102 894-2] follow this time format. 

## **Definition** 

**RS_ARI_10** 

The ‘s _tation clock’_ means a clock representing Cooperative Intelligent Transport Systems (C-ITS) time in a C-ITS station (see RS_RSP_006). 

## **Definition** 

(RS_BSP_429) **RS_ARI_11** 

Information provided with a _‘confidence level’_ of 95 % means that the true value is inside the confidence interval or the confidence area for at least 95 % of the data points in a given statistical base. 

## **Definition** 

(RS_BSP_500) **RS_ARI_12** 

A _‘confidence interval’_ is specified by the estimated value plus/minus the confidence value. 

## **Definition** 

**RS_ARI_13** 

An _‘instant’_ denotes a point on the time axis, often also referred as a ‘moment in time _’_ (see also IEC 60050). 

## **Definition** 

**RS_ARI_15** 

The _‘relevance area’_ (or relevance zone) is the area on the road for which the signage information is applicable. Each separate signage information is associated a specific relevance zone. The concept of an IVI relevance zone is the equivalent of an eventHistory used for DENMs. 

## **Definition** 

**RS_ARI_16** 

The ‘awareness area’ (or detection zone) is the area where drivers have to be informed about upcoming relevant signage information. The concept of an IVI detection zone is the equivalent of a DENM trace. 

## **5 Parameter settings** 

**Table 3: Parameter settings RS_ARI_22** 

|**Parameter**|**Value**|**Unit Description**|**Unit Description**|**Min.**<br>**Value**|**Max.**<br>**Value**|**Source**<br>**Document**|
|---|---|---|---|---|---|---|
|_pRepetitionInterval_|500|ms|Interval for the IVI repetition service|--|--|--|
|_pIdUniquenessRadius_|25|km|Radius around the originating station<br>within which the tuple<br>serviceProviderID-<br>IviIdentificationNumber shall be unique|--|--|--|
|_pIdReuseBlockingTime_|24|H|Minimum blocking time before a<br>previously used IviIdentificationNumber<br>may be reused by a service provider||||
|_pRepetitionDuration_|5|Min|Duration over which a message shall be<br>repeated|**--**|**--**|**--**|
|_pLongitudinalOffsetSig_<br>_nPosition_|3|m|Maximum longitudinal offset to the<br>actual position of the physical sign|**--**|**--**|**--**|
|_pNodeOffset_|1|m|Maximum offset between two nodes<br>describing the same geographical<br>position|**--**|**--**|**--**|
|_pMaxNumberofNodesP_<br>_erZone_|100|--|Maximum number of deltaPositions per<br>segment / zone|**--**|**--**|**--**|
|_pMinDetectionZoneLen_<br>_gth_|800|m|Minimum length of a detection zone for<br>highway use cases|**--**|**--**|**--**|
|_pMaxDetectionZoneLe_<br>_ngth_|2000|m|Maximum length of a detection zone for<br>highway use cases|**--**|**--**|**--**|
|_pLateralNodeOffset_|3|m|Maximum lateral offset to the center of<br>the lane /carriageway for the<br>deltaPositions in polygonalLine and the<br>referencePosition|--|--|--|
|_pLateralNodeOffset_AD|1|m|Maximum lateral offset to the center of<br>the lane /carriageway for the<br>deltaPositions in polygonalLine and the<br>referencePosition  if automated driving<br>shall be supported|--|--|--|
|_pLaneAngleDeviation_|5|°|Maximum angle between the<br>connection of the node points and the<br>corresponding tangent to the lane<br>centre|--|--|--|



|pMaxPerpendDistLane<br>Centre|10|m|Maximum perpendicular distance<br>between the linear connection of two<br>consecutive lane nodes and the actual<br>centre of the lane|--|--|--|
|---|---|---|---|---|---|---|



## **6 General understanding of the IVIM** 

## **6.1 Purpose of the In-Vehicle Signage use cases** 

The purpose of the In-Vehicle Signage (IVS) is to enable the receiving vehicle to know at any time and condition all the relevant signage information, based on time and location, but also based on characteristics and type of the vehicle. Receivers can filter sign information based on time, geographical and other relevance criteria (e.g. to only show information relevant ahead to the driver). 

## **6.2 Purpose of the different containers in IVIM** 

This chapter provides a short introduction to the three most relevant containers in IVIM: Management Container, Geographic Location Container and General IVI Container. See also Figure 1 for a simplified representation of the IVIM. 

**Figure 1: Simplified and shortened representation of IVIM** 

## **6.2.1 Management Container** 

The Management container is mandatory and provides the receiving vehicles with information necessary to handle the entire IVI message, unambiguously identify it ( _ServiceProviderId_ , _iviIdentificationNumber_ ) as well as to decide on its further processing and determine the status and time validity of its content (e.g. iviStatus, timestamp, validFrom, validTo, etc.) 

## **6.2.2 Geographic Location Container** 

The Geographic Location Container (Glc) describes essential information for receiving vehicles to understand where and how the information provided in the IVI Application Container applies. 

It is formed by a part which is common to all the parts of the Application Container plus a sequence of GlcParts that can be specific to the distinct parts of the application container. GlcParts are used to represent detection and relevance zones (following the definitions provided in [C2CCC Glos]). According to C-Roads specifications, at least one detection zone and one relevance zone shall be provided for each IVI message. Each GlcPart is described, among others, by a zoneId (unambiguously identifying the zone), and a Zone (defining the geographical-shape of the zone) 

## **6.2.3 General IVI Container** 

The General IVI Container (Gic) provides the signage information to be processed by vehicles. It is a sequence of _GicParts_ , each defining a given piece of signage information.  This information refers to Glc information for its spatial relevance. For this, each _GicPart_ contains, among others _, detectionZoneID_ and _relevanceZoneId_ lists indicating respectively the detection and relevance zones that apply to this _GicPart_ . Moreover, each _GicPart_ contains the _iviType_ (e.g. regulatory info or other kind of info), optionally the _vehicleCharacteristics_ (i.e. for which kind of vehicles the info applies) and the specific signage information to communicate (e.g. road sign identifiers _roadSignCodes_ or text messages _extraText_ , etc.). 

## **7 Requirement specifications** 

## **7.1 IVIM Automotive Requirements** 

## **7.1.1 Transmission** 

## **Other (informational)** 

**RS_ARI_14** 

The following requirement on IVIM apply in addition to the relevant standards ([TS 103 301 v1.3.1] – to be updated to refer to the new ISO TS 19321:2020, the intention is to use the updated version, [ISO/TS 19321:2020]) and the C-Roads [C-ITS Message Profiles and Parameters, Release 1.7]. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_67** 

IVIM shall be repeated with a repetition interval of _pRepetitionInterval_ . 

Details: 

Tested by: 

## **Other (informational)** 

**RS_ARI_38** 

Signs which indicate the end of a specific or all regulations / restrictions should not be transmitted explicitly as individual signs in an IviStructure. The meaning of these signs is implicitly given through the ending of the relevance zone of corresponding signs. 

If transmitted, all requirements given in this document shall apply. 

Note: It is recommended not to transmit the aforementioned signs separately. One reason being that the relevance zone of such signs could stretch along several kilometres. 

Details: 

Tested by: 

## **7.1.2 IviStructure** 

## **Requirement** 

**RS_ARI_70** 

If the iviStructure corresponds to a physical sign / gantry, it shall provide the legal statement as displayed by the static sign or gantry. 

Note 1: This implies that the IviStructure doesn’t need to exactly represent what is depicted on the gantry/sign but needs to provide all information required to represent the regulation as indicated by the gantry/sign. 

Note 2: In order to support use cases where there is no physical sign, a corresponding suitable requirement may be defined in the future. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_17** 

An IviStructure having an iviStatus other than ‘cancellation’ shall contain at least one instance of GeographicLocationContainer. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_18** 

An IviStructure having an iviStatus other than ‘cancellation’ shall contain at least one instance of GeneralIviContainer. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_19** 

All zones referred to within one GicPart should be contained in one single instance of GeographicLocationContainer within the same IviStructure. 

Note: This implies that each IviStructure shall be self-contained. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_78** 

Requirement RS_ARI_19 is only phrased with ‘should’ since there might be situations when more than one GLC is needed. One example for such a situation could be, when more than one reference position is needed to comply with all corresponding requirements of this document. 

Details: 

Tested by: 

**Requirement** 

**RS_ARI_20** 

The IviStructure should not contain any instances of LayoutContainer and TextContainer. 

Note: If present, these containers may be ignored by receivers. The containers AutomatedVehicleContainer and RoadSurfaceContainer are currently not considered and may therefore also be ignored by receivers. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_21** 

If in vehicle information shall or need to be transmitted in separate IVIMs, the following prioritization shall be applied (number one having the highest priority): 

- 1) Information applying to the same lane should be contained in a single message. 

- 2) Information applying to the same direction of travel should be contained in a single message. 

- 3) Information applying to the same local area should be contained in a single message. 

Details: 

Tested by: 

## **Requirement** 

## **RS_ARI_25** 

If there are multiple physical signs showing the same information applicable to the same road segment (e.g. one in a distance, one directly at the location of danger), only one IviStructure and GicPart shall be transmitted for all signs. 

Details: 

Tested by: 

## **Requirement** 

## **RS_ARI_52** 

At every point in time every combination of RsCode and relevanceZoneIds contained in an IviStructure shall be unique for that IviStructure. 

Note: This means, that the combination of RsCode and relevance zone shall not be duplicated in in more than one IviStructure at any given point in time. This also excludes a situation as shown in Figure 2. 

**Figure 2: No duplicate information in separate IviStructures, example** 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_53** 

All in-vehicle information to be conveyed via IVIM should be transmitted in as few separate IviStructures as possible. 

Details: 

Tested by: 

## **Requirement (preliminary)** 

**RS_ARI_60** 

An IviStructure shall provide the total number of lanes of the concerned direction on the road segment where the zones as described in the IviStructure are located. 

Note: The means how to do this are still in discussion. 

Details: 

Tested by: 

## **7.1.3 ManagementContainer** 

## **Requirement** 

**RS_ARI_58** 

The tuple of ServiceProviderID and IviIdentificationNumber shall be unique at every given point in time within a radius of at least _pIdUniquenessRadius_ around the transmitting C-ITS station. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_59** 

When a service provider has used an iviIdentificationNumber for an IviStructure, a minimum blocking time of at least pIdReuseBlockingTime shall pass before the same iviIdentificationNumber may be used again for another IviStructure with different content by an RSU of the same provider within a distance of pIdUniquenessRadius. This does not apply for transitions in the iviStatus of an iviStructure, which use by definition the same iviIdentificationNumber. 

Note: To cope for overlaps of the geonet destination areas, the radius is designed to be larger than 2x 10 km and contains another buffer of 5 km, resulting in 25 km radius. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_56** 

The timestamp shall be present and set to the time of information generation by the service provider (as defined in [TS 103 301]). 

Note: This also holds, if the iviStatus is already set to ‘update’. When a new content change occurs, timeStamp shall be set to the point in time of the generation of the new information. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_62** 

The component validFrom shall be present in an IviStructure if the contained information is not yet applicable at the point in time when the message is transmitted. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_63** 

The component validFrom shall be omitted in an IviStructure if the contained information is applicable at the point in time when the message is transmitted. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_71** 

The component validTo may only be used to indicate the validity duration of the information contained in the IviStructure, if it is ensured that validTo exceeds the actual validity period. 

Note 1: This means, that validTo shall not be shorter than the actual validity duration of the information. This prevents, that vehicles travelling in the relevance zone wrongly cancel the information to the driver when validTo times out only because an update of the validTo is not received. 

Note 2: Example of a scenario that could benefit from using validTo: Speed limit for purposes of noise reduction over night, e.g. 10 p.m. to 6 a.m. In this scenario the validity duration is deterministic and can be conveyed via validTo thus lifting the need for a separate cancellation message. 

Note 3: Example of a scenario where a different usage than specified here can lead to critical situations: The component validTo is set to a time only some minutes in the future and is updated every time before timing out. In such cases vehicles, that have passed the gantry and are already out of the RSU coverage, but yet in the relevance zone, would disable the received IVI road signs upon reaching the validTo time, even if the RSU has updated the validTo and still transmits the road signs. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_37** 

If in vehicle information shall or need to be transmitted in separate IVIMs following RS_ARI_21 due to message size restrictions, the data element connectedIviStructures shall be present and used to connect at least all messages applying to the same traffic direction. 

Details: 

Tested by: 

## **Other (informational)** 

**RS_ARI_64** 

For better understanding of the following requirements, Figure 3 provides a state machine for the usage of iviStatus including references to the relevant documents and requirements for the respective state transitions. 

**Figure 3: State machine for iviStatus** 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_65** 

An IviStructure with status ‘new’ or ‘update’ shall be repeated as long as all information contained remains unchanged or the time value represented by validTo hasn't yet passed in time. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_66** 

Whenever any signage information changes (meaning any change in the GIVs, TCs or AVCs present in an IviStructure), the IviStructure shall be transmitted with iviStatus ‘update’. 

Note: For any changes in the geographic information see requirement RS_ARI_81. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_81** 

Whenever any geographic information changes (meaning any change in the GLCs, MLCs or RCCs present in an IviStructure), the IviStructure shall be transmitted with iviStatus ‘cancellation’ and a new IviStructure with iviStatus ‘new’ containing the updated geographic information shall be transmitted. 

Note: For any changes in the signage information see requirement RS_ARI_66. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_54** 

Whenever all the information given in an IviStructure is not valid any more (i.e. the gantry is switched off and the information isn’t shown any more), the IviStructure shall be transmitted with iviStatus ‘cancellation’. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_55** 

An IviStructure with status ‘cancellation’ shall be repeated for _pRepetitionDuration_ starting from the point in time of the first transmission of the cancellation IVIM. 

Details: 

Tested by: 

## **Requirement** 

## **RS_ARI_57** 

An IviStructure with status ‘cancellation’ shall consist of the ManagementContainer only. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_82** 

If the gantry is dark (i.e. if no signage information is available in the R-ITS-S) for longer than _pRepetitionDuration_ , no IviStructure shall be transmitted. 

Details: 

Tested by: 

## **Other (informational)** 

**RS_ARI_83** 

In case of any failure or error in the R-ITS-S, no IviStructure shall be transmitted. 

Details: 

Tested by: 

## **7.1.4 Geographic Location Container** 

## **Requirement** 

## **RS_ARI_30** 

If the IviStructure corresponds to a physical sign/gantry, the referencePosition in GLC shall be located in the middle of the carriageway at the position of the sign/gantry. The (longitudinal) offset shall be at most _pLongitudinalOffsetSignPosition_ . (See also RS_ARI_28 ) 

Note: In order to support use cases where there is no physical sign, a corresponding suitable requirement may be defined in the future. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_29** 

The referencePosition in GLC shall be located in the middle of the carriageway with a maximum lateral offset to the true middle of the carriageway of _pLateralNodeOffset._ 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_32** 

An instance of GLC shall consist of at least two GlcParts. 

Note: This ensures that there are at least two zones for representation of detection and relevance zone of information contained in the GeneralIviContainer, respectively. 

Details: 

Tested by: 

## _**7.1.4.1 Geographic Location Container Part**_ 

## **Requirement** 

**RS_ARI_31** 

The zoneId in GlcPart shall be unique throughout the entire IviStructure (i.e. this also applies, if multiple GLCs are used within one IviStructure). 

Note: Uniqueness is only required for the triple serviceProviderID + iviIdentificationNumber + zoneID. Hence, for signage information spread over multiple messages, zoneIDs may be reused. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_39** 

To describe a zone, the component segment shall be used. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_72** 

The number of deltaPositions per segment shall be limited to _pMaxNumberofNodesPerZone_ . 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_40** 

In all instances of IVI.IviStructure.optional.glc.parts.zone.segment.line in an IviStructure, only either the component deltaPositions or the component deltaPositionsWithAltitude shall be used. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_61** 

The first deltaPosition contained in PolygonalLine shall refer to the reference position given in the corresponding GLC. 

Note: See RS_ARI_76 for a better understanding. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_75** 

The referencePosition shall not be part of the zone itself. 

Note 1: This means that the first deltaPosition in a zone shall describe the first node of the respective zone. If a zone shall begin at the referencePosition, the first deltaPosition shall be set to (0, 0). See RS_ARI_74 and RS_ARI_76 for further information. 

Note 2: This requirement is in compliance with ISO/TS 19321:2020, where a note explains that the referencePosition of the GLC is not part of the polygonal line. 

Note 3: Not including the reference position to the zones by default becomes even more important when zones are not directly attached to the reference position (e.g. when considering ramps). 

Details: 

Tested by: 

## **Other (informational)** 

**RS_ARI_76** 

The graphic below shows the problematic implications when including the referencePosition in the zone description. For individual zones per lane the inclusion of the reference position would ‘distort’ the zone causing possible problems for interpretation on vehicle side, therefore the first deltaPosition is considered to be the very first node of the zone. 

**Figure 4: ‘Distortion’ of zones when including the referencePosition** 

Details: 

Tested by: 

## **Other (informational)** 

## **RS_ARI_74** 

Requirements RS_ARI_29, RS_ARI_30, RS_ARI_61 and RS_ARI_75 specify polygonal lines in a very generic way in order for them to be applicable to all possible scenarios and settings. The graphic below shows the implications of these requirements on the affected data elements in IVIM. 

**Figure 5: Placement of the referencePosition and definition of the first deltaPosition** 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_42** 

The delta positions in PolygonalLine shall be sorted starting from the zone’s extremity that is closest to the reference position in ascending order according to the distance to this extremity along the course of the zone. 

Note: That way, zones are always sorted in direction of traffic or against the direction of traffic. See RS_ARI_77 for a better understanding. 

Details: 

Tested by: 

## **Other (informational)** 

## **RS_ARI_77** 

Requirements RS_ARI_42 is phrased in a very generic way. This is necessary for cases where the referencePosition isn’t located at the borders between the zones but actually in the middle of a zone. This occurs for example, when a driverAwarenessZone is used (for driverAwarenessZone, see RS_ARI_26). Without the driverAwarenessZone, the previous requirements make sure that the referencePosition is located at the border between detectionZone and relevanceZone. 

Details: 

Tested by: 

## **Other (informational)** 

(RS_ARSM_31) **RS_ARI_45** 

DeltaPositions in PolygonalLine should correspond to the centre of the lane or carriageway – depending on whether the zone describes a lane or the entire carriageway. 

Details: 

Tested by: 

## **Requirement** 

(RS_ARSM_32) **RS_ARI_46** 

The absolute lateral offset of node points to the centre of the lane or carriageway shall be less than _pLateralNodeOffset_ . 

Details: 

Tested by: 

## **Requirement** 

(RS_ARSM_94) **RS_ARI_47** 

Let 𝑎⃗ be the vector representing the linear connection of two delta positions, and 𝑝 ⃗⃗⃗⃗ be the vector representing the shortest distance of vector 𝑎⃗ to the center of the lane/carriageway (that is, 𝑝⃗ is perpendicular to the tangent of the center line of the lane/carriageway at the foot of the dropped perpendicular). 

Then for |𝑝⃗| > 0 it shall always hold that 

**==> picture [198 x 21] intentionally omitted <==**

For |𝑝⃗| = 0 (i.e. 𝑎⃗ crosses the lane/carriageway centre) the angle α between 𝑎⃗ and the tangent to the lane/carriageway centre at the intersection point with the lane centre shall be less than _pLaneAngleDeviation_ . 

Note: In less formal wording this means that the angle between the linear connection of two node points and the corresponding tangent to the lane/carriageway centre shall not be greater than _pLaneAngleDeviation._ 

Note: See drawings below for a better understanding (exemplary for a polygonalLine describing the centre of the carriageway): 

Details: 

Tested by: 

## **Requirement** 

(RS_ARSM_34) **RS_ARI_48** 

The perpendicular distance between the linear connection of two delta positions and the centre of the lane/carriageway shall be less than _pMaxPerpendDistLaneCentre_ . Details: 

Tested by: 

## **Requirement** 

**RS_ARI_50** 

The data element laneWidth shall be provided if the corresponding zone describes a single lane, and may be used in all other cases. 

Note: For a zone containing more than one lane, according to ISO/TS 19321, the laneWidth represents the overall width of the zone. 

Details: 

Tested by: 

## **7.1.5 MAP Location Container** 

## **Requirement** 

**RS_ARI_37** 

The MAP Location Container shall not be used for highway use cases _._ 

Note: This container may be used at intersections where a MAPEM is transmitted anyway, for such use cases this needs to be profiled explicitly. 

Details: 

Tested by: 

## **7.1.6 General IVI Container Part** 

## **Requirement** 

**RS_ARI_36** 

All zoneIds present in the components detectionZoneIds, driverAwarenessZoneIds and/or relevanceZoneIds within an instance of GicPart shall reference zones which are all described in the same GLC. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_34** 

In every instance of GicPart the data element _detectionZoneIds_ shall be present and contain at least one entry referencing to an existing zone ID in a GLC. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_23** 

Each set of physically consecutive zones referenced by the data element _detectionZoneIds_ shall be defined in such a way that it leads up to the corresponding set of physically consecutive relevance zones. This means that the first point of each set of physically consecutive detection zones shall geographically coincide with the first point in corresponding set of physically consecutive relevance zones a maximum offset of _pNodeOffset_ . 

Note: For a better understanding see the graphics below. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_51** 

Each set of physically consecutive zones referenced by the data element detectionZoneIds in a GicPart shall have an accumulated length of at least _pMinDetectionZoneLength_ . 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_79** 

The set of consecutive zones referenced by the data element detectionZoneIds in GicPart shall cover a distance of at most _pMaxDetectionZoneLength_ . 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_80** 

The set of consecutive zones referenced by the data element detectionZoneIds in GicPart shall be completely contained in the destination area defined in the GeoNet header. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_26** 

An instance of driverAwarenessZoneIds shall be present in all GicParts which refer to a physical sign that is located before the start of the relevance zone. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_27** 

The driver awareness zone in a GicPart (i.e. the combination of all zones referred to in the instance of _driverAwarenessZoneIds_ ) shall represent the complete area between the location of the physical sign and the start of the relevance zone, if the sign’s applicability doesn’t start at the position of the sign but in a certain distance. 

**Figure 6: Example: overtaking ban applicable in a distance - e.g. due to a situation on the road** 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_24** 

If defined, a driver awareness zone shall be part of the detection zone (i.e. geographically contained within the detection zone). 

Details: 

Tested by: 

**Requirement** 

**RS_ARI_35** 

In every instance of GicPart the data element _relevanceZoneIds_ shall be present and refer to a nonempty set of zones described in a GLC. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_69** 

The zoneIDs in the components relevanceZoneIds, detectionZoneIds and driverAwarenessZoneIds shall be ordered in form of a vectorised matrix. 

Note: This means that physically consecutive zones constitute one matrix column and shall be sorted accordingly. See Figure 7 for a better understanding. 

Example 1: All zones shown in the picture constitute one relevanceZone for one sign/information, then the set of zoneIDs in relevanceZoneIds shall be ordered as follows: {37, 49, 4, 12, 85, 23, 178, 19, 7} 

Example 2: (Artificial but illustrative) Zones 37, 12, 178, 49 and 19 constitute the relevance zone, zone 85 is a driverAwarenessZone and zones 85, 4, 23 and 7 constitute the detectionZone for one sign/information. Then the lists of IDs shall be ordered as follows: 

- relevanceZoneIds: {37, 49, 12, 178, 19} 

- driverAwarenessZoneIds: {85} 

- detectionZoneIds: {4, 85, 23, 7} 

**Figure 7: ‘Vectorization’ of zones** 

Details: 

Tested by: 

## **Requirement** 

## **RS_ARI_43** 

For each set of physically consecutive zones (along the path of the road segment) referenced in _relevanceZoneIds_ in an instance of GicPart, there shall be a corresponding set of physically consecutive zones referenced in _detectionZoneIds_ , which fulfils requirement RS_ARI_23 . 

Details: 

Tested by: 

## **Requirement** 

## **RS_ARI_33** 

The relevanceZone in a GicPart (i.e. the combination of all zones referred to in the instance of _relevanceZoneIds_ ) shall represent the complete road segment where the traffic rules according to the sign described in GicPart are applicable. 

Note: If the relevanceZone ends and no further signs are transmitted via IVIMs, this means, that from the last point of the relevanceZone downstream, the previous roadsign transmitted via IVIM doesn’t apply any more. Figure 8 shows an example of a correct implementation, Figure 9 shows a possible receiver interpretation in case of a faulty implementation in the same situation. 

**Figure 8: Example of a correct implementation of relevanceZone** 

**Figure 9: Possible receiver interpretation in case of a faulty implementation** 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_28** 

The longitudinal position w.r.t. the carriageway of the first node of the set of zones referenced by _relevanceZoneIds_ (or by _driverAwarenessZoneIds_ , if used), shall coincide with the longitudinal position of the physical sign (if applicable), with a maximum offset of _pLongitudinalOffsetSignPosition_ if the traffic rule according to the sign is applicable starting from the position of the sign. Note: In this case ‘if applicable’ means, if there is a physical sign present. In case of virtual signage without physical sign this requirement is not applicable. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_44** 

The data element _direction_ shall be present in every instance of GicPart in an IviStructure. 

Details: 

Tested by: 

## **Requirement** 

**RS_ARI_68** 

The component iviType shall be set in accordance with the service categories as defined in ISO 14823. The following mapping shall be used: 

|**iviType**|**Service category**|
|---|---|
|0 (immediateDangerWarningMessages)|11 (Warning), 31 (ambient road condition), 32|
||(road condition)|
|1 (regulatoryMessages)|12 (regulatory)|
|2 (trafficRelatedInformationMessages)|13 (guide)|
|3 (pollutionMessages)|n/a|
|4 (noTrafficRelatedInformationMessages)|21 (public facilities)|



Details: 

Tested by: 

## **Requirement** 

**RS_ARI_73** 

RSCodes that apply to multiple lanes shall occur only once in an IviStructure (i.e. in only one single GicPart) with indication of the concerned lanes in the component applicableLanes. 

Note: This implies that it is not allowed to repeat the same road sign in separate GicParts, each of them associated to a given applicableLane. It serves the purpose of data minimization. 

Details: 

Tested by: 

## **7.2 Open questions and subjects** 

## **7.2.1 Usage of zoneHeading** 

According to current C-Roads specifications, the usage of zoneHeading in GlcPart is mandatory (see [C-ITS Message Profiles and Parameters, Release 1.7], Table 10). 

The profile defines it as ‘Effective direction of applicability of the sign at the Reference Position, indicating the traffic direction’. C2CCC’s understanding is, that this information shall be given through ‘direction’ in GIC. 

Furthermore, it is not clear, how this value will be determined and how it is defined – will it be the heading between the ‘first’ two nodes of the zone? What is the intended added value of this information? E.g. we are not sure if the enabling of a differentiation between the zones on a highway and the zones on a ramp would work in all situations (see figure below). 

**Figure 10: Motorway exit ramp; heading of the first two nodes wouldn't differ from the heading of zones on the motorway (representation simplified to ease understanding)** 

Some clarification in the specifications is needed for us to understand how to make use of the data element. 

## **8 Annex** 

This annex contains a table for IVIM showing which data elements are mandatory according to the standard (CEN/ISO), this document and the C-Roads profile in Release 1.7. 

Legend: 

- The number of ‘+’ in the column ‘Layer’ and the shading of the row represents the layer / level of the corresponding data element within the message. 

- ‘-’: This data element is not mentioned in the respective document. 

- ‘O’: This data element is optional. 

- ‘M’: This data element is mandatory. 

- ‘O/M’: This data element is mandatory only under certain conditions which are defined in the respective document. 

- ‘C’: This data element is an option within a ‘Choice’. 

- ‘NU’: (C-Roads specific) This data element is not used in C-Roads. 

- ‘F’: The respective document forbids the usage of this data element. 

- ‘O/F’: This data element is forbidden under certain conditions which are defined in the respective document. 

- ‘O/F/M’: This data element is mandatory only under certain conditions and forbidden und other conditions which are defined in the respective document. 

## **8.1 IVIM mandatory and optional data elements** 

|Layer|Data element / data field in and<br>IviStructure|ISO 19321 C2C-CC|ISO 19321 C2C-CC<br>(this<br>document)|C-Roads<br>(Release 1.7)|
|---|---|---|---|---|
|+|managementContainer|M|-|M|
|++|serviceProviderId|M|M|M|
|++|iviIdentificationNumber|M|M|M|
|++|timeStamp|O|M|M|
|++|validFrom|O|O/F/M|O|
|++|validTo|O|O/F|M|
|++|connectedIviStructures|O|O/M|NU|
|++|iviStatus|M|M|M|
|++|connectedDenms|O|-|-|
|+|iviContainers (sequence of<br>IviContainer)|O|O/M|M|
|++|geographicLocationContainer|C|O/M|M|



|+++<br>~~—|~~|referencePosition<br>~~|~~|M<br>|M<br>|M<br>|M<br>|
|---|---|---|---|---|---|
|++++<br>~~—|~~|latitude<br>~~|~~|M<br>|-<br>|-<br>|M<br>|
|++++<br>~~— |—~~|longitude<br>~~|—~~<br>~~|~~|M<br>~~—~~<br>~~|~~|-<br>~~—~~<br>~~|~~<br>~~ee~~|-<br>~~—~~<br>~~|~~<br>~~ee~~|M<br>~~—~~<br>~~|~~|
|++++<br>~~a~~|positionConfidenceEllipse<br>~~a~~<br>~~ee~~|M<br>~~a~~<br>~~ee~~|-<br>~~a~~<br>~~ee~~<br>~~ee~~|-<br>~~a~~<br>~~ee~~<br>~~ee~~|M<br>~~a~~<br>~~ee~~|
|++++|altitude|M|-<br>~~ee~~|-<br>~~ee~~|M|
|+++|referencePositionTime|O|-|NU||
|+++|referencePositionHeading|O|-|NU||
|+++|referencePositionSpeed|O|-|NU||
|+++|parts (sequence of GlcParts)|M|M|M|M|
|++++<br>~~—~~<br>~~**|**~~<br>~~—~~|zoneId<br>~~—~~<br>~~|~~<br>~~**|**~~<br>|M<br>~~—~~<br>~~|~~|M<br>~~—~~<br>~~|~~|M<br>~~—~~<br>~~|~~|M<br>~~—~~<br>~~|~~|
|++++<br>~~—~~<br>~~**|**~~<br>~~—~~|laneNumber<br>~~—~~<br>~~**|**~~<br>|O<br>~~—~~|-<br>~~—~~|O/M<br>~~—~~|O/M<br>~~—~~|
|++++<br>~~**|**~~<br>~~——|~~|zoneExtension<br>~~**|**~~<br>~~|~~|O|-|NU||
|++++<br>~~—|~~|zoneHeading<br>~~|~~|O|-|M|M|
|++++<br>~~— |~~<br>~~a~~|zone<br>~~|~~<br>~~ee~~|O<br>~~ee~~|M<br>~~ee~~|M<br>~~ee~~|M<br>~~ee~~|
|+++++<br>~~a~~<br>~~a~~|segment<br>|C<br>|M<br>~~ee~~<br>|M<br>|M<br>|
|++++++<br>~~a~~<br>~~a~~|line<br>~~ee~~<br>|M<br>~~ee~~<br>|M<br>~~ee~~<br>~~ee~~<br>|M<br>~~ee~~<br>|M<br>~~ee~~<br>|
|+++++++<br>~~a~~|deltaPosition<br>~~ee~~|C<br>~~ee~~|C<br>~~ee~~<br>~~ee~~|M<br>~~ee~~|M<br>~~ee~~|
|+++++++<br>~~a~~|deltaPositionsWithAltitude<br>~~ee~~|C<br>~~ee~~|C<br>~~ee~~|?<br>~~ee~~|?<br>~~ee~~|
|+++++++<br>~~a~~|absolutePositions<br>~~ee~~|C<br>~~ee~~|F<br>~~ee~~|F<br>~~ee~~|F<br>~~ee~~|
|+++++++<br>~~a~~<br>~~a~~|absolutePositionsWithAltitude<br>|C<br>|F<br>~~ee~~<br>|F<br>|F<br>|
|++++++<br>~~a~~<br>~~a~~<br>~~a~~|laneWidth<br>~~ee~~<br><br>|O<br>~~ee~~<br><br>|O/M<br>~~ee~~<br>~~ee~~<br><br>|O/M<br>~~ee~~<br><br>~~ee~~<br>|O/M<br>~~ee~~<br><br>~~ee~~<br>|
|+++++<br>~~a~~<br>~~a~~|area<br>~~ee~~<br>|C<br>~~ee~~<br>|-<br>~~ee~~<br>~~ee~~<br>|F<br>~~ee~~<br>~~ee~~<br>|F<br>~~ee~~<br>~~ee~~<br>|
|++++++<br>~~a~~|…<br>~~ee~~|~~ee~~|~~ee~~|~~ee~~<br>~~ee~~|~~ee~~<br>~~ee~~|
|+++++<br>~~a~~|computedSegment<br>~~ee~~|C<br>~~ee~~|-<br>~~ee~~<br>~~ee~~|F<br>~~ee~~<br>~~eee~~|F<br>~~ee~~<br>~~eee~~|
|++++++<br>~~ee~~|…<br>~~ee~~|~~ee~~|~~ee~~<br>~~ee~~|~~ee~~<br>~~eee~~|~~ee~~<br>~~eee~~|
|++|generalIviContainer (sequence<br>of GicParts)|C|O/M<br>~~ee ~~|C/M<br> ~~eee~~|O/M<br>~~eee~~|
|+++|detectionZoneIds|O|M|M|M|



|+++|Its-Rrid|O|-|NU||
|---|---|---|---|---|---|
|+++|relevanceZoneIds|O|M|M|M|
|+++|direction|O|M|M|M|
|+++|driverAwarenessZoneIds|O|O/M|NU|O/M|
|+++|minimumAwarenessTime|O|-|NU||
|+++|applicableLanes|O|-|O/M|O/M|
|+++|iviType|M|M|M|M|
|+++|iviPurpose|O|-|NU||
|+++|laneStatus|O|-|O|O|
|+++|vehicleCharacteristics|O|-|O|O|
|++++|…|||||
|+++|driverCharacteristics|O|-|NU||
|+++|layoutId|O|-|NU||
|+++|preStoredlayoutId|O|-|NU||
|+++|roadSignCodes (sequence of<br>RSCode|M|M|M|M|
|++++|layoutComponentId|O|-|O|O|
|++++<br>~~a~~|code<br>~~ee~~|M<br>~~ee~~|-<br>~~ee~~|M<br>~~ee~~|M<br>~~ee~~|
|+++++<br>~~a~~<br>~~a~~|viennaConvention<br>~~ee~~|C<br>~~ee~~|-<br>~~ee~~<br>~~ee~~|F<br>~~ee~~|F<br>~~ee~~|
|++++++<br>~~a~~<br>~~a~~<br>~~a~~|…<br>~~ee~~<br>~~ee~~|~~ee~~<br>~~ee~~|~~ee~~<br>~~ee~~<br>~~ee~~|~~ee~~<br>~~ee~~|~~ee~~<br>~~ee~~|
|+++++<br>~~a~~|iso14823|C|-<br>~~ee~~|M|M|
|++++++<br>~~a~~|…<br>~~ee~~|~~ee~~|~~ee~~|~~ee~~|~~ee~~|
|+++++<br>~~a~~<br>~~a~~|itisCodes<br>~~ee~~|C<br>~~ee~~|-<br>~~ee~~<br>~~ee~~|F<br>~~ee~~|F<br>~~ee~~|
|++++++<br>~~a~~<br>~~a~~|…<br>~~ee~~|~~ee~~|~~ee~~<br>~~ee~~|~~ee~~|~~ee~~|
|+++++<br>~~a~~<br>~~a~~|anyCatalogue<br>~~ee~~|C<br>~~ee~~|-<br>~~ee~~<br>~~ee~~|F<br>~~ee~~|F<br>~~ee~~|
|++++++<br>~~a~~|…<br>~~ee~~|~~ee~~|~~ee~~|~~ee~~|~~ee~~|
|+++<br>~~a~~<br>~~_~~|extraText (sequence of Text)<br>~~ee ~~|O<br> ~~ee~~<br>~~|~~|-<br>~~ee~~<br>~~|~~|O<br>~~ee~~<br>|O<br>~~ee~~|
|++++<br>~~_~~|layoutComponentId|O<br>~~|~~|-<br>~~||~~|M* (due to<br>error in<br>~~|~~|O*|



|||||previous ISO<br>version)|
|---|---|---|---|---|
|++++|language|M|-|-|
|++++|textContent|M|-|-|
|++|roadConfigurationContainer|C|-|NU|
|+++|…||||
|++|textContainer|C|F|NU|
|+++|…||||
|++|layoutContainer|C|F|NU|
|+++|…||||
|++|automatedVehicleContainer|C|-|NU|
|+++|…||||
|++|mapLocationContainer|C|F|NU|
|+++|…||||
|++|roadSurfaceContainer|C|-|NU|
|+++|…||||



