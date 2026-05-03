from qrels import qrels


RUNS = {
    "bm25": {
        "q1_software_engineer_5y": [
            "7667d04e-ac78-502c-92c2-ed6290a350a0",
            "04da1f18-bea8-50d4-a290-2a14998ba2a4",
            "5e359491-9615-5c12-acf5-1e5e8bcef600",
            "37d7b4ab-0272-5dc6-9f7f-09012b902554",
            "66a3f389-a029-5f0a-92f5-53d0be6feffb",
        ],
        "q2_frontend_react": [
            "d064c1e2-4cf1-5cd1-808b-74d355fd41c5",
            "bd65e5e5-1657-561b-8128-c085a647be28",
            "43e2d6a1-ec64-5abc-9cef-be135543a9a7",
            "5783dac0-9c32-5e71-be35-c3a950418e75",
            "c12948ba-80a0-5340-ae92-1f1e81d3d3ed",
        ],
        "q3_python_machine_learning": [
            "00b3a663-66ca-5a47-bccd-ffd91b14bcb7",
            "b8329ab9-64a7-5488-ac5d-a0f59f93ba5a",
            "31f191e1-682a-5ccc-a87f-b7c6e90fdae6",
            "8ed92a0f-1604-5afa-806a-f615e645dd97",
            "5d5f7c4e-25d9-560a-b99e-4f84f948504c",
        ],
        "q4_cybersecurity_penetration_testing": [
            "a424c9d2-7e0c-5ab6-a5f4-87b4797a96d9",
            "5efd01f9-fc7c-5994-9637-4e901e8d7e40",
            "a090aa8a-9956-50bf-98f3-eaa0c342868a",
            "99245de6-e725-5424-9b1e-b7082a0bbc3f",
            "89c03e6a-29f1-501c-896e-4b306d2e1ec1",
        ],
        "q5_mid_level_project_managers_3_5y": [
            "43feb20a-eb3a-59df-b0f7-b05114164807",
            "73c69d01-b6d4-5955-931f-1412d814e1c3",
            "893d7a7e-6eaf-5d25-9504-cc02d969af9f",
            "202ce274-2240-5f75-9cfc-7a52c3b21862",
            "9684083c-28f3-5146-937a-a71a8e1511fa",
        ],
        "q6_legal_consultants_10y": [
            "4b9b5489-e6d0-5263-acfe-4ecca173d659",
            "9ca900fd-920e-5193-9c21-10f762a34389",
            "f677d278-82aa-5280-87c2-8efaa4965cab",
            "f21320eb-63d7-5a25-b2c1-2e721843c46e",
            "5d8e7f94-89c4-5cb8-8fc5-972065118330",
        ],
        "q7_healthcare_clinical": [
            "839129f3-e5c2-5cf1-88bd-a33436ce0fec",
            "cbbbc55e-f627-561f-8ebe-3f3e7161c575",
            "c9042c4e-fe0d-5beb-8bd6-7de50e8bb546",
            "1ac0e658-3ad0-5f3d-9b67-729ae64a0ccd",
            "2be860a5-3e61-5253-b6e4-01e1cd161958",
        ],
        "q8_fintech_blockchain": [
            "2157e915-7a61-5718-be8b-550a6d913886",
            "4e78cec0-d1eb-50d7-a491-7b96611941de",
            "27aa65c5-ad50-5da8-860c-a670971ae949",
            "0ae87bda-363c-5d43-a20d-3ceebc40f82a",
            "21a7857b-14f6-5612-9c66-bed0db92d522",
        ],
        "q9_developers_based_in_europe": [
            "cd19fae9-e14f-5c90-abc3-6b7cbcab9ab5",
            "eebcdeae-a58f-52f6-9984-b9033fe37145",
            "cda2d0ff-d86b-5525-b28b-5af0b1cf36f5",
            "8abb06c2-2546-5e40-aaec-9f72fc078376",
            "88c57556-7b19-5267-8b1c-df9daf1687e4",
        ],
        "q10_remote_customer_support": [
            "510543eb-df32-5c9c-a5db-9f33787ea708",
            "8462ee4e-ef9f-5d09-a07d-160886bdf44f",
            "59af781b-1e83-51c5-9a8f-969aaba9465f",
            "00b730ec-261a-5643-bb49-738b94c34ef4",
            "8f5cf92e-c346-581f-8eb5-b979e07ff004",
        ],
        "q11_aws_certified_solutions_architects": [
            "e38c9a46-bc08-5066-b25a-00a387320c8c",
            "9dee9552-92d2-5b84-ab62-07f1c0a57140",
            "aa998a0d-a4fd-5e87-aa8f-921bcef0d133",
            "1b5fb9be-035b-55b5-bd27-85f7b13cc742",
            "89c03e6a-29f1-501c-896e-4b306d2e1ec1",
        ],
        "q12_cybersecurity_certifications": [
            "1c3a62dd-7c6c-57b8-b6d3-867a6f386e5b",
            "0bd75370-7625-5822-b297-3556f48f71f5",
            "35e22be4-cd6d-5d28-8453-1312e3db3da6",
            "f8ff53be-8bf3-56f3-9033-1cafcc4d2037",
            "be3157fb-9d77-58f9-83b2-c364b7356c3c",
        ],
        "q13_strong_leadership": [
            "7d57d844-6743-55a3-a29d-7912e79e1782",
            "0c38c180-64c0-58c9-8f69-8fb003c77fb5",
            "6934927f-1986-546b-985e-4585bac62876",
            "b27dd8c4-7769-54e7-81d0-dec691dd5b13",
            "8c0dc964-4bfe-5068-8238-8638383e9a89",
        ],
        "q14_excellent_communication": [
            "0942451d-7fa6-5cb6-803c-ef4acedbaca8",
            "a4d2f7a9-c54b-5cc0-a651-83f8621d5470",
            "b3c41891-75aa-508a-ad4c-b5ca87dee180",
            "14ee04a1-02c3-5329-a070-7cd0f435c771",
            "1223c7d1-8729-5db2-85af-20ac93ae601a",
        ],
        "q15_docker_kubernetes": [
            "669a18f9-3055-5142-a32b-fa770f384dda",
            "a6457ecb-527c-55d7-96b8-53faf5db12d4",
            "e0b35bbc-4129-5dfa-86bd-6235231ec572",
            "b41cb12f-dc6d-55f6-bd76-a9ca49211e28",
            "dac6f39d-431d-5da3-a679-b790cc93e557",
        ],
        "q16_qa_selenium": [
            "6b62e693-5a56-571d-85b7-5433a83105d6",
            "d488284b-305c-5d0b-9cb7-6956512bbd4e",
            "7b7f7f89-ed5e-591f-8958-4ef7258805e3",
            "d4286268-8ed7-5e3e-8705-b32ea0f8d135",
            "52e4eda7-7efb-5cbf-953e-a6efe41a877c",
        ],
        "q17_python_fintech_europe": [
            "7c499ac7-a392-5058-b1e1-73dae9e0d911",
            "a83a88c8-bd52-5524-ae40-0560d2604185",
            "ab1bed98-d00f-534d-962d-1c14a8c93be2",
            "bf667b12-0c23-57aa-80c6-86d2a7377503",
            "bf6aaabc-15d2-59fc-911f-21f30b8f0181",
        ],
        "q18_ai_nlp": [
            "73b82115-4767-5fc3-9a12-2d04f9993e74",
            "a7c69f12-7ae0-502a-a3d5-2cc194d27a5f",
            "0fcee886-8992-56e2-b6de-183ce88ae083",
            "179b7847-3f1e-56e5-a9a2-6ef308b434ca",
            "c497ff01-2363-5c69-b80d-0c1bdd15141c",
        ],
        "q19_multilingual_english_greek_french": [
            "6e84b1de-38c1-5155-921a-cf010bdd868e",
            "d90e2af0-600d-5f66-a172-2e9611d14b66",
            "3f08ae6c-47c2-5850-9994-a905c19e9aed",
            "57ba9cfe-eba0-5130-ad3e-731dcbf15b33",
            "b6ec2563-3561-517f-8924-b6a1d5686fdb",
        ],
        "q20_no_degree_strong_experience": [
            "f608c4c2-a5f6-55cb-9c8d-621c0ef5d42f",
            "7d57d844-6743-55a3-a29d-7912e79e1782",
            "9ccc1164-8891-511c-a9be-ea00c3a9c3c7",
            "a25fa440-fe6f-55d2-8221-526e6fcd7e91",
            "d095fa7d-c0e4-59b9-a614-58beafd100c6",
        ],
    },

    "dense": {
        "q1_software_engineer_5y": [
            "3864fecc-2a67-5058-a918-8bbdd47eb44e",
            "fb5039c4-9421-5e48-b868-da33aed6c07a",
            "acce9555-ddd9-5240-bf7d-5dc0bab49c42",
            "6eeb1706-6c66-5d91-b068-e77c2821a802",
            "257c85d9-7654-52a4-a47c-f35db8e61284",
        ],
        "q2_frontend_react": [
            "41fa20c4-32e5-5bb2-81e0-c08c18b828dd",
            "6841139b-1d66-53db-b185-91830554b98b",
            "bd65e5e5-1657-561b-8128-c085a647be28",
            "5f166ab5-e5c5-5115-9fb4-02e1a24c965d",
            "4244dbad-7a59-57d1-9dcb-e802c66973e3",
        ],
        "q3_python_machine_learning": [
            "4a08875a-0f59-5978-85e2-c3837ba13e14",
            "31f191e1-682a-5ccc-a87f-b7c6e90fdae6",
            "8ed92a0f-1604-5afa-806a-f615e645dd97",
            "48b2306c-87e0-5539-b1bb-55d47d8a704b",
            "7d15575c-54ad-5c9c-8b07-0a08caf0a60b",
        ],
        "q4_cybersecurity_penetration_testing": [
            "a090aa8a-9956-50bf-98f3-eaa0c342868a",
            "a424c9d2-7e0c-5ab6-a5f4-87b4797a96d9",
            "89c03e6a-29f1-501c-896e-4b306d2e1ec1",
            "5efd01f9-fc7c-5994-9637-4e901e8d7e40",
            "9f35153a-388d-59ad-946c-aeb4a8a8631c",
        ],
        "q5_mid_level_project_managers_3_5y": [
            "02bf08ad-a1b4-565d-83b7-6a8ff142ad08",
            "0e411996-8f8e-54a3-a0f4-ffe1a7cf5196",
            "f1da9348-38c5-56eb-880e-c6072ad66e25",
            "a1bb6110-faf5-5889-9c34-e54b2b788004",
            "fbab4e71-3251-5dec-a1c1-e7eecf887d4b",
        ],
        "q6_legal_consultants_10y": [
            "ae28ca07-74ec-5836-b830-057b82ecdd37",
            "9ca900fd-920e-5193-9c21-10f762a34389",
            "e3f59ac5-8ac7-5200-98be-260c827f66d4",
            "09ac16ff-4db1-564a-87e3-4bbddfcfebcb",
            "7bd07147-1736-514d-bf31-8aaaa9865700",
        ],
        "q7_healthcare_clinical": [
            "0f5ec9cb-f297-5df8-af33-a84ad038cc16",
            "839129f3-e5c2-5cf1-88bd-a33436ce0fec",
            "edd21664-31fc-54c4-94d5-71fbc0424f0c",
            "1ac0e658-3ad0-5f3d-9b67-729ae64a0ccd",
            "30fc39db-6210-5b83-9b62-3317580c70bb",
        ],
        "q8_fintech_blockchain": [
            "f2a67593-e988-5f41-999f-5f6194665e3f",
            "27aa65c5-ad50-5da8-860c-a670971ae949",
            "40dab5b7-9bf0-5b35-872f-976bee155db9",
            "27c2bd69-7d5c-5801-921f-51f3c54d76a5",
            "ffd0a648-595c-5dc5-8df4-13000ac090d1",
        ],
        "q9_developers_based_in_europe": [
            "770666b2-284b-5924-a741-97b1522fbe85",
            "3fd9f426-93a7-5475-ab69-d043850d2f1f",
            "320f6886-36ac-58ba-9232-c847f5d830b5",
            "eb2bf765-c122-5b93-a7fd-4d50695351bf",
            "c69b8733-1c0c-5053-8d7d-23d901fa7dd6",
        ],
        "q10_remote_customer_support": [
            "73d30da6-f620-5fcc-afcb-4c0dcdd63e9f",
            "abf53ffe-ffb4-5334-ac6b-cd4eaf7542f5",
            "8f5cf92e-c346-581f-8eb5-b979e07ff004",
            "4ccf1ee9-8f1d-5979-ad83-631304db90ab",
            "b5f65f52-e4ef-590b-9676-4ee6e5a00065",
        ],
        "q11_aws_certified_solutions_architects": [
            "85be9a5b-f1ac-5baa-8d3a-7a78d0eaa66e",
            "ec79d01e-0a3b-544c-a4dc-0e7f7ab04803",
            "8a46779b-6ce5-56e0-8ca8-a40a20ef9f69",
            "d9b59ac7-4295-5411-995b-0ac76c292eea",
            "e7d87d7c-c79f-5738-a4fc-1627ad0968de",
        ],
        "q12_cybersecurity_certifications": [
            "9f35153a-388d-59ad-946c-aeb4a8a8631c",
            "e01e5ab0-2237-5e8d-8273-9cfe78c1c2e4",
            "85b47665-4b87-55ec-8c18-3bb74e4e2aa1",
            "c6df262a-b4e3-561d-ba1c-e6d4769071dc",
            "a090aa8a-9956-50bf-98f3-eaa0c342868a",
        ],
        "q13_strong_leadership": [
            "613be193-55d0-508c-bc41-ddec6fb09322",
            "d43ca241-0671-50b3-bb97-27c02811bfd7",
            "8c0dc964-4bfe-5068-8238-8638383e9a89",
            "242d2b6e-e6f5-5a0a-8cc6-49ba53d57c6e",
            "09c249c2-6f73-51f2-9292-6a2b69524cd6",
        ],
        "q14_excellent_communication": [
            "44db329c-1486-56a8-8560-ad42e4c3bdc3",
            "feef0c79-2cf2-5a3e-8f43-ffa2c2c1d723",
            "c7c4f900-bbf4-5729-ab19-b7b5421ece3a",
            "b099490e-480e-589a-a740-3f5ad8caf19e",
            "c9da6011-42b3-5dfb-9438-9c019f260884",
        ],
        "q15_docker_kubernetes": [
            "43d39247-b070-58b4-95e1-ff563ec8e483",
            "93e2449e-0c30-53fe-a0d4-19b7d3189f8b",
            "bb45e8e1-fca8-51a4-b5f7-320f06f9f1d0",
            "766c0eae-06ed-527d-91ef-ad9400f69fe9",
            "669a18f9-3055-5142-a32b-fa770f384dda",
        ],
        "q16_qa_selenium": [
            "4548f446-b5aa-56f3-a36c-fe303df00387",
            "9019bf99-4a6e-50df-9562-512fd9dc8f94",
            "4b7222bb-bb07-5333-9026-0f449c1dcd80",
            "c67aab28-cd90-57d2-9403-568a05ff99bb",
            "1caf7e7d-78d2-50c4-8634-7611091ddaf9",
        ],
        "q17_python_fintech_europe": [
            "f98293ad-92e8-5975-a654-c3a84437a6ea",
            "5d993c6e-f537-51c3-bfb9-fe0928c32515",
            "e65863c2-7b45-5dc8-b67e-626fb2cc2355",
            "efea38d1-994f-513e-bbf2-a4b933128638",
            "c5c07c61-23ca-56c8-af89-363b4f62bd4f",
        ],
        "q18_ai_nlp": [
            "70cf95f0-17db-50e4-bcdd-67e6f896735d",
            "af20ec8f-29fb-5a22-99a6-40888d19b4fd",
            "48efc621-4742-51b2-9fcb-a1ae9cc1da29",
            "afb1af95-a250-514c-9a88-ba93bd6a22be",
            "69fbe99d-1cde-5c59-924b-9c20ab7a8860",
        ],
        "q19_multilingual_english_greek_french": [
            "91cbf3a4-b10b-5dea-bb6b-a5a3dadd5abe",
            "2c49e352-7f84-5f75-8adb-6db1f6c1f002",
            "458f2bf2-0396-54df-ae1f-5a6f2c0176f7",
            "0577e27b-9e67-5299-a767-b13ecdcd00a9",
            "ba5e94a3-f7e9-5486-b22c-42153c689bf3",
        ],
        "q20_no_degree_strong_experience": [
            "7d57d844-6743-55a3-a29d-7912e79e1782",
            "ff175dc4-9303-5c72-9a78-2f36e902665c",
            "8ded01be-9d33-5fcf-a185-9ca3732b357c",
            "72fe2a30-ca07-5322-99a0-617bc3907c6a",
            "1fc1b5c0-377a-5ea8-96d7-13ff3b3f862c",
        ],
    },
}


def precision_at_k(results, query_qrels, k):
    retrieved = results[:k]
    relevant = sum(query_qrels.get(doc_id, 0) for doc_id in retrieved)
    return relevant / k


def recall_at_k(results, query_qrels, k):
    retrieved = results[:k]
    relevant_retrieved = sum(query_qrels.get(doc_id, 0) for doc_id in retrieved)
    total_relevant = sum(query_qrels.values())

    if total_relevant == 0:
        return 0.0

    return relevant_retrieved / total_relevant


def mrr(results, query_qrels):
    for rank, doc_id in enumerate(results, start=1):
        if query_qrels.get(doc_id, 0) == 1:
            return 1 / rank
    return 0.0


def average_precision(results, query_qrels):
    relevant_found = 0
    precision_sum = 0.0
    total_relevant = sum(query_qrels.values())

    if total_relevant == 0:
        return 0.0

    for rank, doc_id in enumerate(results, start=1):
        if query_qrels.get(doc_id, 0) == 1:
            relevant_found += 1
            precision_sum += relevant_found / rank

    return precision_sum / total_relevant


def evaluate_run(run_name, run_results, k=5):
    print(f"\n=== {run_name.upper()} EVALUATION ===")

    p_scores = []
    r_scores = []
    mrr_scores = []
    ap_scores = []

    for query_id, results in run_results.items():
        query_qrels = qrels[query_id]

        p = precision_at_k(results, query_qrels, k)
        r = recall_at_k(results, query_qrels, k)
        rr = mrr(results, query_qrels)
        ap = average_precision(results, query_qrels)

        p_scores.append(p)
        r_scores.append(r)
        mrr_scores.append(rr)
        ap_scores.append(ap)

        print(f"\nQuery: {query_id}")
        print(f"Precision@{k}: {p:.3f}")
        print(f"Recall@{k}:    {r:.3f}")
        print(f"MRR:           {rr:.3f}")
        print(f"AP:            {ap:.3f}")

    print("\n--- AVERAGE RESULTS ---")
    print(f"Mean Precision@{k}: {sum(p_scores) / len(p_scores):.3f}")
    print(f"Mean Recall@{k}:    {sum(r_scores) / len(r_scores):.3f}")
    print(f"Mean MRR:           {sum(mrr_scores) / len(mrr_scores):.3f}")
    print(f"MAP:                {sum(ap_scores) / len(ap_scores):.3f}")


if __name__ == "__main__":
    for run_name, run_results in RUNS.items():
        evaluate_run(run_name, run_results, k=5)