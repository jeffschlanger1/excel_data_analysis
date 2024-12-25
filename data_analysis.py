import streamlit as st
import pandas as pd

st.title("Data Analysis Dashboard")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    cdc_data = None
    uof_data = None
    uof_subject = None
    traffic_data = None
    non_traffic_data = None
    custodial_arrests_data = None
    complaints_data = None
    commendations_data = None
    pursuits_data = None

    try:
        cdc_data = pd.read_excel(uploaded_file, sheet_name="CDC")
    except ValueError:
        print("Sheet 'CDC' not found.")

    try:
        uof_data = pd.read_excel(uploaded_file, sheet_name="UOF Overview")
    except ValueError:
        print("Sheet 'UOF Overview' not found.")

    try:
        uof_subject = pd.read_excel(uploaded_file, sheet_name="UOF Subject")
    except ValueError:
        print("Sheet 'UOF Subject' not found.")

    try:
        traffic_data = pd.read_excel(uploaded_file, sheet_name="Traffic Citations")
    except ValueError:
        print("Sheet 'Traffic Citations' not found.")

    try:
        non_traffic_data = pd.read_excel(uploaded_file, sheet_name="Non-Traffic Citations")
    except ValueError:
        print("Sheet 'Non-Traffic Citations' not found.")

    try:
        custodial_arrests_data = pd.read_excel(uploaded_file, sheet_name="Custodial Arrest")
    except ValueError:
        print("Sheet 'Custodial Arrest' not found.")

    try:
        complaints_data = pd.read_excel(uploaded_file, sheet_name="Complaints")
    except ValueError:
        print("Sheet 'Complaints' not found.")

    try:
        commendations_data = pd.read_excel(uploaded_file, sheet_name="Commendation")
    except ValueError:
        print("Sheet 'Commendation' not found.")

    try:
        pursuits_data = pd.read_excel(uploaded_file, sheet_name="Vehicle Pursuits")
    except ValueError:
        print("Sheet 'Vehicle Pursuits' not found.")

    st.success("File uploaded and all sheets loaded successfully!")

    if st.button("Process"):
        with st.spinner("Processing... Please wait."):

            if not cdc_data.empty:
            
                # Event creation (Concatenate Columns BI and BJ)
                cdc_data['Event'] = cdc_data['Column1.Event Information  Case Number Prefix'].astype(str) + ' ' + cdc_data['Column1.Event Information  Case Number'].astype(str)

                # Totals
                total_forms = len(cdc_data)
                total_calls = cdc_data[cdc_data['Column1.Event Information  Initiation'] == "Call for Service/Dispatch"].shape[0]
                total_proactive = cdc_data[cdc_data['Column1.Event Information  Initiation'] == "Pro-Active Contact"].shape[0]

                st.metric("Total Number of Forms Completed", total_forms)
                st.metric("Total Number of Calls for Service/Dispatch", total_calls)
                st.metric("Total Number of Pro-active Contacts", total_proactive)

                # Force Metrics
                total_use_of_force = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Did you use force with t'] == " Yes (APD Tier 0/1/2 Incident)"].shape[0]
                tier_0 = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used'] == "Tier 0"].shape[0]
                tier_0_firearm = cdc_data[(cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used'] == "Tier 0") & (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Type of Force You Used'] == '["Firearm"]')].shape[0]
                tier_1 = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used'] == "Tier 1"].shape[0]
                tier_2 = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used'] == "Tier 2"].shape[0]

                st.metric("Total Number of Use of Force Incidents", total_use_of_force)
                st.metric("Total Number Tier 0", tier_0)
                st.metric("Total Number Tier 0 with Firearm", tier_0_firearm)
                st.metric("Total Number Tier 1", tier_1)
                st.metric("Total Number Tier 2", tier_2)

                # Demographic Breakdown
                non_hispanic_white = cdc_data[(cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Race'] == "White") & (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Ethnic'] == "Non-Hispanic")].shape[0]
                black = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Race'] == "Black"].shape[0]
                hispanic = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Ethnic'] == "Hispanic"].shape[0]
                others = cdc_data[~cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Race'].isin(["White", "Black"]) | ~cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Ethnic'].isin(["Hispanic", "Non-Hispanic"])].shape[0]

                st.metric("Total Non-Hispanic Whites", non_hispanic_white)
                st.metric("Total Black", black)
                st.metric("Total Hispanic", hispanic)
                st.metric("Total Others", others)

                # Activity Types
                traffic_stops = cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Reason for Contact'].count()
                unlawful_activity = cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Suspected Crime'].count()
                terry_stops = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Did you conduct a Terry '] == "Yes"].shape[0]

                st.metric("Total Traffic Stops", traffic_stops)
                st.metric("Total Responses to Unlawful Activity", unlawful_activity)
                st.metric("Total Terry Stops", terry_stops)

                # Activity Outcomes
                arrests = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Result of Contact'] == '["Arrest"]'].shape[0]
                warnings = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Result of Contact'] == '["Warning"]'].shape[0]
                no_action = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Result of Contact'] == '["No Action – if selected, choose no other options"]'].shape[0]
                citations = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Result of Contact'] == '["Citation"]'].shape[0]
                searches_conducted = cdc_data[cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Conducted Search or Prop'] == "Yes"].shape[0]

                st.metric("Total Arrests", arrests)
                st.metric("Total Warnings", warnings)
                st.metric("Total No Actions", no_action)
                st.metric("Total Citations", citations)
                st.metric("Total Searches Conducted", searches_conducted)

                st.subheader("Officer-Level Analysis")
                officer_data = cdc_data.groupby('Column1.submittedBy').agg(
                    Calls_for_Service=('Column1.Event Information  Initiation', lambda x: (x == 'Call for Service/Dispatch').sum()),
                    Proactive_Contacts=('Column1.Event Information  Initiation', lambda x: (x == 'Pro-Active Contact').sum()),
                    Use_of_Force=('Column1.Citizen Contact Information repeaterRepeater434.Did you use force with t', lambda x: (x == ' Yes (APD Tier 0/1/2 Incident)').sum()),
                    Tier_0=('Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used', lambda x: (x == 'Tier 0').sum()),
                    Tier_0_Firearm=('Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used', lambda x: ((x == 'Tier 0') & (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Type of Force You Used'] == '["Firearm"]')).sum()),
                    Tier_1=('Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used', lambda x: (x == 'Tier 1').sum()),
                    Tier_2=('Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used', lambda x: (x == 'Tier 2').sum()),
                    Non_Hispanic_White=('Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Race', lambda x: ((x == 'White') & (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Ethnic'] == 'Non-Hispanic')).sum()),
                    Black=('Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Race', lambda x: (x == 'Black').sum()),
                    Hispanic=('Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Ethnic', lambda x: (x == 'Hispanic').sum()),
                    Other=('Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Race', lambda x: ((x.isin(['ASIAN', 'Other', 'Mixed Race'])).sum())),
                    Traffic_Stops=('Column1.Citizen Contact Information repeaterRepeater434.Reason for Contact', lambda x: x.notnull().sum()),
                    Unlawful_Activity=('Column1.Citizen Contact Information repeaterRepeater434.Suspected Crime', lambda x: x.notnull().sum()),
                    Terry_Stops=('Column1.Citizen Contact Information repeaterRepeater434.Did you conduct a Terry ', lambda x: (x == 'Yes').sum()),
                    Arrests=('Column1.Citizen Contact Information repeaterRepeater434.Result of Contact', lambda x: (x == '["Arrest"]').sum()),
                    Warnings=('Column1.Citizen Contact Information repeaterRepeater434.Result of Contact', lambda x: (x == '["Warning"]').sum()),
                    No_Action=('Column1.Citizen Contact Information repeaterRepeater434.Result of Contact', lambda x: (x == '["No Action – if selected, choose no other options"]').sum()),
                    Citations=('Column1.Citizen Contact Information repeaterRepeater434.Result of Contact', lambda x: (x == '["Citation"]').sum()),
                    Searches=('Column1.Citizen Contact Information repeaterRepeater434.Conducted Search or Prop', lambda x: (x == 'Yes').sum())
                ).reset_index()

                # Formatting table with headers
                st.dataframe(officer_data)

                st.subheader("For Review")
                # Filter conditions
                terry_stop_review = (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Did you conduct a Terry '] == 'Yes') & (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Result of Contact'].isin(['["No Action – if selected, choose no other options"]', '["Warning"]']))
                traffic_stop_review = cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Reason for Contact'].notnull() & cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Result of Contact'].isin(['["No Action – if selected, choose no other options"]', '["Warning"]'])
                tier_0_firearm_review = (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Tier Level of Force Used'] == 'Tier 0') & (cdc_data['Column1.Citizen Contact Information repeaterRepeater434.Type of Force You Used'] == '["Firearm"]')

                # Combine all conditions into one DataFrame
                for_review = cdc_data.loc[terry_stop_review | traffic_stop_review | tier_0_firearm_review].copy()

                # Add a "Reason for Review" column to explain why each entry is included
                for_review['Reason for Review'] = (
                    terry_stop_review.map(lambda x: 'Terry Stop: No Action or Warning' if x else '') +
                    traffic_stop_review.map(lambda x: 'Traffic Stop: No Action or Warning' if x else '') +
                    tier_0_firearm_review.map(lambda x: 'Tier 0 with Firearm' if x else '')
                )

                # Drop empty "Reason for Review" rows and clean up
                for_review = for_review[for_review['Reason for Review'] != '']

                # Display the table
                st.dataframe(for_review)


            if not uof_data.empty:
                # UOF Overview Sheet
                st.subheader("2. UOF Overview By Officer")

                # Calculate totals for Tier 1 and Tier 2
                tier_1_total = (uof_data['Tier Level'] == 'Tier 1').sum()
                tier_2_total = (uof_data['Tier Level'] == 'Tier 2').sum()

                # Group by Officer and calculate totals
                by_officer = uof_data.groupby('Sworn Member Name')['Tier Level'].value_counts().unstack(fill_value=0)

                # Tier 1 Primary and Other
                tier_1_primary = ((uof_data['Tier Level'] == 'Tier 1') & (uof_data['Sworn Member Role in UoF'] == 'Primary Officer')).sum()
                tier_1_other = ((uof_data['Tier Level'] == 'Tier 1') & (uof_data['Sworn Member Role in UoF'].isin(['Secondary/Assisting Officer', 'Sworn Member Witness']))).sum()

                # Tier 2 Primary and Other
                tier_2_primary = ((uof_data['Tier Level'] == 'Tier 2') & (uof_data['Sworn Member Role in UoF'] == 'Primary Officer')).sum()
                tier_2_other = ((uof_data['Tier Level'] == 'Tier 2') & (uof_data['Sworn Member Role in UoF'].isin(['Secondary/Assisting Officer', 'Sworn Member Witness']))).sum()

                # Display the overview
                st.write(f"### UOF Totals")
                st.write(f"- **Tier 1 Total**: {tier_1_total}")
                st.write(f"- **Tier 2 Total**: {tier_2_total}")
                st.write(f"- **Tier 1 Primary**: {tier_1_primary}")
                st.write(f"- **Tier 1 Other**: {tier_1_other}")
                st.write(f"- **Tier 2 Primary**: {tier_2_primary}")
                st.write(f"- **Tier 2 Other**: {tier_2_other}")

                # Display data by Officer
                st.write("### Totals by Officer")
                st.dataframe(by_officer)

                st.header("Categorize Data by Officer")

                tier_1_primary = (uof_data['Tier Level'] == 'Tier 1') & (uof_data['Sworn Member Role in UoF'] == 'Primary Officer')
                tier_1_other = (uof_data['Tier Level'] == 'Tier 1') & (uof_data['Sworn Member Role in UoF'].isin(['Secondary/Assisting Officer', 'Sworn Member Witness']))
                tier_2_primary = (uof_data['Tier Level'] == 'Tier 2') & (uof_data['Sworn Member Role in UoF'] == 'Primary Officer')
                tier_2_other = (uof_data['Tier Level'] == 'Tier 2') & (uof_data['Sworn Member Role in UoF'].isin(['Secondary/Assisting Officer', 'Sworn Member Witness']))

                # Group by Officer (Column E) and calculate the sums for each category
                grouped = uof_data.groupby('Sworn Member Name').agg(
                    Tier_1_Primary=('Sworn Member Role in UoF', lambda x: (tier_1_primary.loc[x.index]).sum()),
                    Tier_1_Other=('Sworn Member Role in UoF', lambda x: (tier_1_other.loc[x.index]).sum()),
                    Tier_2_Primary=('Sworn Member Role in UoF', lambda x: (tier_2_primary.loc[x.index]).sum()),
                    Tier_2_Other=('Sworn Member Role in UoF', lambda x: (tier_2_other.loc[x.index]).sum())
                ).reset_index()
                st.dataframe(grouped)

            # if not uof_subject.empty:

            #     st.header("3. UOF Subject")
            #     # Concatenate Event Date (Column G) and Event Time (Column H)
            #     uof_subject['Event Date and Time'] = uof_subject['Event Information Case Number Prefix'].astype(str) + ' ' + uof_subject['Event Information Case Number'].astype(str)

            #     # Calculations for totals
            #     totals = {
            #         'Total Uses of Force': len(uof_subject),
            #         'Total Tier 1': len(uof_subject[uof_subject['Tier Level'] == 'Tier 1']),
            #         'Total Tier 2': len(uof_subject[uof_subject['Tier Level'] == 'Tier 2']),
            #         'Total Subjects Injured': uof_subject['Subject Injured During UoF Incident'].sum(),  
            #         'Total Felonies': len(uof_subject[uof_subject['Charge Level'] == 'Felony']),  
            #         'Total Misdemeanors': len(uof_subject[uof_subject['Charge Level'] == 'Misdemeanor']),  
            #     }

            #     # Demographic Breakdown
            #     demographic_breakdown = {
            #         'Total Number of Non-Hispanic Whites': len(uof_subject[uof_subject['Race Expansion'] == 'White / European']),
            #         'Total Number of Black': len(uof_subject[uof_subject['Race Expansion'] == 'Black / African American']),
            #         'Total Number of Hispanic': len(uof_subject[uof_subject['Race Expansion'] == 'Hispanic']),
            #         'Total Number of Others': len(uof_subject[uof_subject['Race Expansion'].isin(['ASIAN', 'Other', 'Mixed Race'])]),
            #     }

            #     # Display totals and demographic breakdown
            #     st.header("Totals")
            #     st.write(totals)

            #     st.header("Demographic Breakdown")
            #     st.write(demographic_breakdown)

            #     # Tier Level breakdown by demographics
            #     tier_demographics = uof_subject.groupby(['Tier Level', 'Race Expansion']).size().unstack(fill_value=0)

            #     st.header("Tier Level Breakdown by Demographics")
            #     st.dataframe(tier_demographics)


            #     st.header("UOF Subject By Officer")

            #     # Step 1: Concatenate Event Date (Column G) and Event Time (Column H) to create a unique Event identifier
            #     uof_subject['Event Date and Time'] = uof_subject['Event Information Case Number Prefix'].astype(str) + ' ' + uof_subject['Event Information Case Number'].astype(str)
            #     uof_data['Event Date and Time'] = uof_data['Event Information Case Number Prefix'].astype(str) + ' ' + uof_data['Event Information Case Number'].astype(str)

            #     # Step 2: Merge UOF Overview with UOF Subject to get Officer Name based on concatenated Event identifier
            #     merged_data = pd.merge(uof_subject, uof_data[['Event Date and Time', 'Sworn Member Name']],
            #                         on='Event Date and Time', how='inner')

            #     # Step 3: Filter officers with at least one UOF
            #     officers_with_uof = merged_data['Sworn Member Name'].value_counts()
            #     officers_with_uof = officers_with_uof[officers_with_uof > 0]  # Ensure non-zero UOF counts

            #     # Step 4: Prepare breakdown for each officer
            #     officer_breakdown = []

            #     for officer in officers_with_uof.index:
            #         officer_data = merged_data[merged_data['Sworn Member Name'] == officer]
                    
            #         # Totals for the officer
            #         total_uof = len(officer_data)
            #         total_tier_1 = len(officer_data[officer_data['Tier Level'] == 'Tier 1'])
            #         total_tier_2 = len(officer_data[officer_data['Tier Level'] == 'Tier 2'])
            #         total_injured = officer_data['Subject Injured During UoF Incident'].sum()
            #         total_felonies = len(officer_data[officer_data['Charge Level'] == 'Felony'])
            #         total_misdemeanors = len(officer_data[officer_data['Charge Level'] == 'Misdemeanor'])
                    
            #         # Demographic Breakdown for the officer
            #         demographics = {
            #             'Non-Hispanic White': len(officer_data[officer_data['Race Expansion'] == 'White / European']),
            #             'Black': len(officer_data[officer_data['Race Expansion'] == 'Black / African American']),
            #             'Hispanic': len(officer_data[officer_data['Race Expansion'] == 'Hispanic']),
            #             'Other': len(officer_data[officer_data['Race Expansion'].isin(['ASIAN', 'Other', 'Mixed Race'])]),
            #         }
                    
            #         # Append breakdown to list (demographics as single column)
            #         officer_breakdown.append({
            #             'Officer Name': officer,
            #             'Total Uses of Force': total_uof,
            #             'Total Tier 1': total_tier_1,
            #             'Total Tier 2': total_tier_2,
            #             'Total Subjects Injured': total_injured,
            #             'Total Felonies': total_felonies,
            #             'Total Misdemeanors': total_misdemeanors,
            #             'Demographic Breakdown': f"Non-Hispanic White: {demographics['Non-Hispanic White']}, "
            #                                     f"Black: {demographics['Black']}, "
            #                                     f"Hispanic: {demographics['Hispanic']}, "
            #                                     f"Other: {demographics['Other']}"
            #         })

            #     # Step 5: Convert breakdown to DataFrame
            #     officer_breakdown_df = pd.DataFrame(officer_breakdown)

            #     # Step 6: Display the officer breakdown
            #     st.header("Officer Breakdown")
            #     st.dataframe(officer_breakdown_df)


            if not traffic_data.empty:
                st.header("Traffic Citations Total")

                traffic_data['Date and Time'] = traffic_data['Occurred Date'].astype(str) + ' ' + traffic_data['Occurred Time'].astype(str)
                
                # Calculate totals
                total_citations = len(traffic_data)  
                unique_stops = traffic_data['Agency Summons Number'].nunique()  
                total_by_charge = traffic_data['Charge'].value_counts()  
                
                # Demographic breakdown
                total_white = (traffic_data['Race Modified'] == 'WHITE').sum()
                total_black = (traffic_data['Race Modified'] == 'BLACK/AFRICAN AMERICAN').sum()
                total_hispanic = (traffic_data['Race Modified'] == 'HISPANIC').sum()
                total_others = traffic_data['Race Modified'].isin(['ASIAN', 'Other', 'Mixed Race']).sum()
                
                # Display results
                st.write(f"**Total Traffic Citations:** {total_citations}")
                st.write(f"**Total Number of Unique Stops:** {unique_stops}")
                st.write("**Total by Each Charge:**")
                st.dataframe(total_by_charge)

                st.header("Demographic Breakdown")
                st.write(f"**Total Number of White:** {total_white}")
                st.write(f"**Total Number of Black:** {total_black}")
                st.write(f"**Total Number of Hispanic:** {total_hispanic}")
                st.write(f"**Total Number of Others (ASIAN, Other, Mixed Race):** {total_others}")

                # Demographic breakdown for each Charge (single column)
                st.header("Demographic Breakdown by Charge")
                by_charge_with_demographics = traffic_data.groupby('Charge').agg(
                    Total_Charges=('Charge', 'size'),
                    Demographics=('Race Modified',
                                lambda x: f"White: {(x == 'WHITE').sum()}, "
                                            f"Black: {(x == 'BLACK/AFRICAN AMERICAN').sum()}, "
                                            f"Hispanic: {(x == 'HISPANIC').sum()}, "
                                            f"Others: {x.isin(['ASIAN', 'Other', 'Mixed Race']).sum()}")
                ).reset_index()
                st.dataframe(by_charge_with_demographics)

                st.header("Traffic Citations Totals By Officer")
                traffic_data['Date and Time'] = traffic_data['Occurred Date'].astype(str) + ' ' + traffic_data['Occurred Time'].astype(str)
                
                # Calculate totals
                total_citations = len(traffic_data)  
                unique_stops = traffic_data['Agency Summons Number'].nunique()  
                total_by_charge = traffic_data['Charge'].value_counts()  
                
                # Demographic breakdown
                total_white = (traffic_data['Race Modified'] == 'WHITE').sum()
                total_black = (traffic_data['Race Modified'] == 'BLACK/AFRICAN AMERICAN').sum()
                total_hispanic = (traffic_data['Race Modified'] == 'HISPANIC').sum()
                total_others = traffic_data['Race Modified'].isin(['ASIAN', 'Other', 'Mixed Race']).sum()
                

                # Demographic breakdown for each Charge
                by_charge_with_demographics = traffic_data.groupby('Charge').agg(
                    Total_Charges=('Charge', 'size'),
                    Total_White=('Race Modified', lambda x: (x == 'WHITE').sum()),
                    Total_Black=('Race Modified', lambda x: (x == 'BLACK/AFRICAN AMERICAN').sum()),
                    Total_Hispanic=('Race Modified', lambda x: (x == 'HISPANIC').sum()),
                    Total_Others=('Race Modified', lambda x: x.isin(['ASIAN', 'Other', 'Mixed Race']).sum())
                ).reset_index()

                # By Officer with combined demographics
                st.header("Demographic Breakdown by Officer")
                by_officer = traffic_data.groupby('Officer Name').agg(
                    Total_Traffic_Citations=('Officer Name', 'size'),
                    Total_Unique_Stops=('Agency Summons Number', pd.Series.nunique),
                    Demographics=('Race Modified',
                                lambda x: f"White: {(x == 'WHITE').sum()}, "
                                            f"Black: {(x == 'BLACK/AFRICAN AMERICAN').sum()}, "
                                            f"Hispanic: {(x == 'HISPANIC').sum()}, "
                                            f"Others: {x.isin(['ASIAN', 'Other', 'Mixed Race']).sum()}")
                ).reset_index()
                st.dataframe(by_officer)

                # Display results
                st.header("Traffic Citations Totals")
                st.write(f"**Total Traffic Citations:** {total_citations}")
                st.write(f"**Total Number of Unique Stops:** {unique_stops}")

                st.write("**Total by Each Charge:**")
                st.dataframe(total_by_charge)

                st.write("**Demographics Breakdown for Each Charge:**")
                st.dataframe(by_charge_with_demographics)

                st.header("Demographic Breakdown")
                st.write(f"**Total Number of White:** {total_white}")
                st.write(f"**Total Number of Black:** {total_black}")
                st.write(f"**Total Number of Hispanic:** {total_hispanic}")
                st.write(f"**Total Number of Others (ASIAN, Other, Mixed Race):** {total_others}")
                
                # st.header("Traffic Citations by Officer")
                # st.dataframe(by_officer)


            if not non_traffic_data.empty:
                st.header("Non-Traffic Citations Totals")

                non_traffic_data['Date and Time'] = non_traffic_data['Occurred Date'].astype(str) + ' ' + non_traffic_data['Occurred Time'].astype(str)
                # non_traffic_data['Date and Time'] = non_traffic_data['Occurred Date'].astype(str)
                
                # Calculate totals
                total_non_traffic_citations = len(non_traffic_data)  
                unique_citations = non_traffic_data['Agency Summons Number'].nunique()  
                total_by_charge = non_traffic_data['Charge'].value_counts()  
                
                # Demographic breakdown
                total_white = (non_traffic_data['Race Modified'] == 'WHITE').sum()
                total_black = (non_traffic_data['Race Modified'] == 'BLACK/AFRICAN AMERICAN').sum()
                total_hispanic = (non_traffic_data['Race Modified'] == 'HISPANIC').sum()
                total_others = non_traffic_data['Race Modified'].isin(['ASIAN', 'Other', 'Mixed Race']).sum()


                # Non-Traffic Citations Totals by Officer with Combined Demographics
                st.header("Non-Traffic Citations Analysis by Officer")
                grouped_by_officer = non_traffic_data.groupby('Officer Name').agg(
                    Total_Citations=('Officer Name', 'size'),
                    Total_Unique_Events=('Agency Summons Number', pd.Series.nunique),
                    Demographics=('Race Modified', 
                                lambda x: f"White: {(x == 'WHITE').sum()}, "
                                            f"Black: {(x == 'BLACK/AFRICAN AMERICAN').sum()}, "
                                            f"Hispanic: {(x == 'HISPANIC').sum()}, "
                                            f"Others: {x.isin(['ASIAN', 'Other', 'Mixed Race']).sum()}")
                ).reset_index()

                st.dataframe(grouped_by_officer)

                st.header("NON Traffic Analysis by Officer")
                # non_traffic_data['Date and Time'] = non_traffic_data['Occurred Date'].astype(str) + ' ' + non_traffic_data['Occurred Time'].astype(str)
                non_traffic_data['Date and Time'] = non_traffic_data['Occurred Date'].astype(str)

                # Calculate totals
                total_non_traffic_citations = len(non_traffic_data)  
                unique_citations = non_traffic_data['Agency Summons Number'].nunique()  
                total_by_charge = non_traffic_data['Charge'].value_counts()  
                
                # Demographic breakdown
                total_black = (non_traffic_data['Race Modified'] == 'BLACK/AFRICAN AMERICAN').sum()
                total_hispanic = (non_traffic_data['Race Modified'] == 'HISPANIC').sum()
                total_others = non_traffic_data['Race Modified'].isin(['ASIAN', 'Other', 'Mixed Race']).sum()
                

                charges_by_officer = non_traffic_data.pivot_table(
                    index='Officer Name',        # Rows (Officer Name)
                    columns='Charge',            # Columns (Unique Charges)
                    values='Agency Summons Number',  # Values to count
                    aggfunc='count',             # Count of citations per charge
                    fill_value=0                 # Replace NaN with 0
                ).reset_index()

                # Non-Traffic Analysis by Charge with Combined Demographics
                st.header("Non-Traffic Citations Analysis by Charge Demographics")
                by_charge_with_demographics = non_traffic_data.groupby('Charge').agg(
                    Total_Charges=('Charge', 'size'),
                    Demographics=('Race Modified',
                                lambda x: f"White: {(x == 'WHITE').sum()}, "
                                            f"Black: {(x == 'BLACK/AFRICAN AMERICAN').sum()}, "
                                            f"Hispanic: {(x == 'HISPANIC').sum()}, "
                                            f"Others: {x.isin(['ASIAN', 'Other', 'Mixed Race']).sum()}")
                ).reset_index()

                st.dataframe(by_charge_with_demographics)
                
                # st.header("Non-Traffic Citations by Officer")
                # st.write("Each column represents a charge with counts per officer:")
                # st.dataframe(charges_by_officer)

                st.header("Non-Traffic Citations Analysis by Officer Demographics")
                st.dataframe(grouped_by_officer)


            if not custodial_arrests_data.empty:
                st.header("Custodial Arrests Totals")
                custodial_arrests_data['Date'] = pd.to_datetime(custodial_arrests_data['Arrest Date']).dt.date
                custodial_arrests_data['Time'] = pd.to_datetime(custodial_arrests_data['Arrest Time']).dt.time

                # Calculate totals
                total_custodial_arrests = len(custodial_arrests_data)  
                total_unique_incidents = custodial_arrests_data['GO Case Number'].nunique()  
                total_felonies = (custodial_arrests_data['Felony/Misdemeanor'] == 'Felony').sum()  
                total_misdemeanors = (custodial_arrests_data['Felony/Misdemeanor'] == 'Misdemeanor').sum()  

                # Demographic breakdown
                total_white = (custodial_arrests_data['Race'] == 'WHITE').sum()
                total_black = (custodial_arrests_data['Race'] == 'BLACK/AFRICAN AMERICAN').sum()
                total_hispanic = (custodial_arrests_data['Race'] == 'HISPANIC OR LATINO').sum()
                total_others = custodial_arrests_data['Race'].isin(['ASIAN', 'Other', 'Mixed Race']).sum()

                # Total by Each Charge (value counts in charge column)
                # total_by_each_charge = custodial_arrests_data['Felony/Misdemeanor'].value_counts()

                # Total by Each Charge (with demographics)
                demographic_by_charge = custodial_arrests_data.groupby(['Felony/Misdemeanor', 'Race']).size().unstack(fill_value=0)


                # Display results
                # st.header("Custodial Arrests Totals")
                st.write(f"**Total Custodial Arrests:** {total_custodial_arrests}")
                st.write(f"**Total Unique Incidents:** {total_unique_incidents}")
                st.write(f"**Total Felonies:** {total_felonies}")
                st.write(f"**Total Misdemeanors:** {total_misdemeanors}")

                st.header("Demographic Breakdown")
                st.write(f"**Total Number of White:** {total_white}")
                st.write(f"**Total Number of Black:** {total_black}")
                st.write(f"**Total Number of Hispanic:** {total_hispanic}")
                st.write(f"**Total Number of Others (ASIAN, Other, Mixed Race):** {total_others}")

                st.header("Demographic Breakdown by Charge")
                st.dataframe(demographic_by_charge)


                # Custodial Arrests Totals by Officer with demographics
                st.header("Custodial Arrests Totals By Officer Demographics")
                by_officer = custodial_arrests_data.groupby('Officer Name').agg(
                    Total_Arrests=('Officer Name', 'count'),
                    Total_Felonies=('Felony/Misdemeanor', lambda x: (x == 'Felony').sum()),
                    Total_Misdemeanors=('Felony/Misdemeanor', lambda x: (x == 'Misdemeanor').sum()),
                    Total_White=('Race', lambda x: (x == 'WHITE').sum()),
                    Total_Black=('Race', lambda x: (x == 'BLACK/AFRICAN AMERICAN').sum()),
                    Total_Hispanic=('Race', lambda x: (x == 'HISPANIC OR LATINO').sum()),
                    Total_Others=('Race', lambda x: x.isin(['ASIAN', 'Other', 'Mixed Race']).sum())
                ).reset_index()
                
                # Add dynamic URL column using the 'GO Case Number'
                def generate_case_url(case_number):
                    formatted_case = f"24-{case_number[-6:]}"  # Extract last 6 digits and prepend '24-'
                    return f"https://app.forcemetrics.ai/app/6ba58613/incident/{formatted_case}?query={case_number}&dateRange=all_time"

                # Assuming 'GO Case Number' is in custodial_arrests_data
                by_officer = by_officer.merge(custodial_arrests_data[['Officer Name', 'GO Case Number']], on='Officer Name', how='left')
                by_officer['Case_URL'] = by_officer['GO Case Number'].apply(generate_case_url)

                # Display the updated dataframe
                st.header("Custodial Arrests Totals By Officer")
                st.dataframe(by_officer)
            
            if not complaints_data.empty:
                ## complaints ##
                # complaints_data['Date_Time'] = complaints_data['Incident Date'].astype(str) + " " + complaints_data['Incident Time'].astype(str)
                complaints_data['Date_Time'] = complaints_data['Incident Date'].astype(str)

                # Total number of complaints
                total_complaints = complaints_data.shape[0]

                # Total unique complaints (Unique Column C values)
                total_unique_complaints = complaints_data['AIM Incident Number'].nunique()

                # Total Open and Closed Complaints (Assuming Column B has 'Open' or 'Closed' values)
                total_open_complaints = complaints_data[complaints_data['Incident Status'] == 'Open'].shape[0]
                total_closed_complaints = complaints_data[complaints_data['Incident Status'] == 'Closed'].shape[0]

                # Total unique officers involved
                unique_officers = complaints_data['Officer Name'].nunique()

                # Total for each finding in Column T
                findings_counts = complaints_data['Finding'].value_counts()

                # Complaint type breakdown in Column G
                complaint_type_counts = complaints_data['Call Type'].value_counts()

                # Display results
                st.header("Complaints Analysis")
                st.write(f"**Total Complaints:** {total_complaints}")
                st.write(f"**Total Unique Complaints:** {total_unique_complaints}")
                st.write(f"**Total Open Complaints:** {total_open_complaints}")
                st.write(f"**Total Closed Complaints:** {total_closed_complaints}")
                st.write(f"**Total Unique Officers Involved:** {unique_officers}")

                st.subheader("Findings Breakdown")
                st.dataframe(findings_counts)

                st.subheader("Complaint Type Breakdown")
                st.dataframe(complaint_type_counts)

                ### Complaint by officer ##

                complaints_by_officer = complaints_data.groupby('Officer Name').agg(
                    Total_Complaints=('Officer Name', 'count'),
                    Unique_Complaints=('AIM Incident Number', 'nunique'),
                    Open_Complaints=('Incident Status', lambda x: (x == 'Open').sum()),
                    Closed_Complaints=('Incident Status', lambda x: (x == 'Closed').sum()),
                    Exonerated=('Finding', lambda x: (x == 'Exonerated').sum()),
                    Not_Sustained=('Finding', lambda x: (x == 'Not Sustained').sum()),
                    Pending=('Finding', lambda x: (x == 'Pending').sum()),
                    Sustained=('Finding', lambda x: (x == 'Sustained').sum()),
                    Unfounded=('Finding', lambda x: (x == 'Unfounded').sum()),
                    Arrest_of_Member=('Call Type', lambda x: (x == 'Arrest of Member').sum()),
                    Citizen_Inquiry=('Call Type', lambda x: (x == "Citizen's Inquiry").sum()),
                    Complaint=('Call Type', lambda x: (x == 'Complaint').sum()),
                    Dept_Directives_Violation=('Call Type', lambda x: (x == 'Dept Directives Violation').sum()),
                    Duty_Related=('Call Type', lambda x: (x == 'Duty Related').sum()),
                    Missed_Court=('Call Type', lambda x: (x == 'Missed Court').sum()),
                    Officer_Professionalism=('Call Type', lambda x: (x == 'Officer Professionalism Issue').sum()),
                    Officer_Rudeness=('Call Type', lambda x: (x == 'Officer Rudeness').sum())
                ).reset_index()

                # Filter to show only officers with at least one complaint
                complaints_by_officer = complaints_by_officer[complaints_by_officer['Total_Complaints'] > 0]

                # Display results
                st.header("Complaints by Officer")
                st.dataframe(complaints_by_officer)


            if not commendations_data.empty:
                ## Commedation data ##

                # commendations_data['Date_Time'] = commendations_data['Incident Date'].astype(str) + " " + commendations_data['Incident Time'].astype(str)

                # Totals
                total_commendations = len(commendations_data)
                unique_commendations = commendations_data['Incident Number'].nunique()

                # Group by Officer (Column K)
                commendations_by_officer = commendations_data.groupby('Officer Name').agg(
                    Total_Commendations=('Officer Name', 'count'),
                    Unique_Commendations=('Incident Number', 'nunique')
                ).reset_index()

                # Display totals
                st.header("Commendations Totals")
                st.write(f"**Total Number of Commendations:** {total_commendations}")
                st.write(f"**Number of Unique Commendations:** {unique_commendations}")

                # Display breakdown by officer
                st.header("Commendations by Officer")
                st.dataframe(commendations_by_officer)

            if not pursuits_data.empty:
                ## Vehicle Pursuits ##

                pursuits_data['Date_Time'] = pursuits_data['INCIDENT DATE'].astype(str) + " " + pursuits_data['Incident Time'].astype(str)
            
                # Totals
                total_pursuits = len(pursuits_data)

                # Display totals
                st.header("Vehicle Pursuits Totals")
                st.write(f"**Total Number of Pursuits:** {total_pursuits}")

            # Display the full processed dataset
            # st.header("Processed Vehicle Pursuits Data")
            # st.dataframe(pursuits_data)

            # Initialize the combined DataFrame
            combined_data = pd.DataFrame(columns=[
                "Activity Type", "Date", "Time", "Officer Name", "Event Number", 
                "Race of Involved Civilian", "Additional Info 1"
            ])
            # Populate combined DataFrame with data from each sheet
            # CDC
            cdc_temp = pd.DataFrame({
                "Activity Type": "CDC",
                "Date": cdc_data["Column1.Event Information  Date of Incident"],  
                "Time": cdc_data["Column1.Event Information  Time of Incident(use 24 hour time format)"],  
                "Officer Name": cdc_data["Column1.submittedBy"],  
                "Event Number": cdc_data["Column1.formNumber"],  
                "Race of Involved Civilian": cdc_data["Column1.Citizen Contact Information repeaterRepeater434.Contact Perceived Race"],  
                "Additional Info 1": cdc_data["Column1.Citizen Contact Information repeaterRepeater434.Did you use force with t"],  
            })
            # UOF Overview
            uof_temp = pd.DataFrame({
                "Activity Type": "UOF Overview",
                "Date": uof_data["Incident Date"],  
                "Time": uof_data["Incident Time"],  
                "Officer Name": uof_data["Sworn Member Name"],  
                "Event Number": uof_data["Case Number"],  
                # "Race of Involved Civilian": uof_data["Column P"], 
                "Additional Info 1": uof_data["Tier Level"],  
            })

            # Traffic Citations
            traffic_temp = pd.DataFrame({
                "Activity Type": "Traffic Citations",
                "Date": traffic_data["Occurred Date"],  
                "Time": traffic_data["Occurred Time"],  
                "Officer Name": traffic_data["Officer Name"],  
                "Event Number": traffic_data["Agency Summons Number"],  
                "Race of Involved Civilian": traffic_data["Race Modified"],  
                "Additional Info 1": traffic_data["Charge"], 
            })

            # Non-Traffic Citations
            non_traffic_temp = pd.DataFrame({
                "Activity Type": "Non-Traffic Citations",
                # "Date": non_traffic_data["Occurred Date"],  
                # "Time": non_traffic_data["Occurred Time"],  
                "Officer Name": non_traffic_data["Officer Name"],  
                "Event Number": non_traffic_data["Agency Summons Number"],  
                "Race of Involved Civilian": non_traffic_data["Race Modified"],  
                "Additional Info 1": non_traffic_data["Charge"],  
            })

            # Arrest Data
            arrest_temp = pd.DataFrame({
                "Activity Type": "Custodial Arrests",
                "Date": custodial_arrests_data["Arrest Date"],  
                "Time": custodial_arrests_data["Arrest Time"], 
                "Officer Name": custodial_arrests_data["Officer Name"], 
                "Event Number": custodial_arrests_data["GO Case Number"],  
                "Race of Involved Civilian": custodial_arrests_data["Race"],  
                "Additional Info 1": custodial_arrests_data["Felony/Misdemeanor"],  
            })

            # if uof_subject:
            #     # Combine all into one DataFrame
            #     combined_data = pd.concat([
            #         cdc_temp, uof_temp, traffic_temp, non_traffic_temp, arrest_temp
            #     ], ignore_index=True)
            # else:
            #     # Combine all into one DataFrame
            #     combined_data = pd.concat([
            #         cdc_temp, traffic_temp, non_traffic_temp, arrest_temp
            #     ], ignore_index=True)

            # Combine all into one DataFrame
            combined_data = pd.concat([
                cdc_temp, traffic_temp, non_traffic_temp, arrest_temp
            ], ignore_index=True)
            # Display the combined DataFrame
            st.header("Combined Data")
            st.dataframe(combined_data)

            # Initialize a dictionary to hold aggregated data
            officer_data = {}

            # Helper function to update counts
            def update_officer_data(officer_name, column, value=1):
                if officer_name not in officer_data:
                    officer_data[officer_name] = {col: 0 for col in ["Total Days Worked", 
                                                                    "Total CDC Forms", 
                                                                    "Total Uses of Force", 
                                                                    "Total Traffic Citations", 
                                                                    "Total Non-Traffic Citations", 
                                                                    "Total Arrests", 
                                                                    # "Total Pursuits", 
                                                                    "Total Complaints", 
                                                                    "Total Commendations"]}
                officer_data[officer_name][column] += value

            # Process CDC data
            for _, row in cdc_data.iterrows():
                update_officer_data(row["Column1.submittedBy"], "Total CDC Forms")  
                update_officer_data(row["Column1.submittedBy"], "Total Days Worked")  

            # Process UOF Overview data
            for _, row in uof_data.iterrows():
                update_officer_data(row["Sworn Member Name"], "Total Uses of Force")  

            # Process Traffic Citations data
            for _, row in traffic_data.iterrows():
                update_officer_data(row["Officer Name"], "Total Traffic Citations")  

            # Process Non-Traffic Citations data
            for _, row in non_traffic_data.iterrows():
                update_officer_data(row["Officer Name"], "Total Non-Traffic Citations") 

            # Process Arrests data
            for _, row in custodial_arrests_data.iterrows():
                update_officer_data(row["Officer Name"], "Total Arrests")  

            # Process Pursuits data
            # for _, row in pursuits_data.iterrows():
            #     update_officer_data(row["Column K"], "Total Pursuits") 

            # Process Complaints data
            for _, row in complaints_data.iterrows():
                update_officer_data(row["Officer Name"], "Total Complaints")  

            # Process Commendations data
            for _, row in commendations_data.iterrows():
                update_officer_data(row["Officer Name"], "Total Commendations")  

            # Convert aggregated officer data to a DataFrame
            officer_summary = pd.DataFrame.from_dict(officer_data, orient="index").reset_index()
            officer_summary.rename(columns={"index": "Officer Name"}, inplace=True)

            # Display the results
            st.header("Summary by Officer")
            st.dataframe(officer_summary)

        st.success("Analysis completed!")


else:
    st.info("Please upload an Excel file to start analysis.")