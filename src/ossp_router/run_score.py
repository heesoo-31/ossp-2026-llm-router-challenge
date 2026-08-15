{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "3f41d5ae-06fc-4e06-a793-7cbda732cd9e",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'ossp_router'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[6], line 9\u001b[0m\n\u001b[1;32m      6\u001b[0m \u001b[38;5;66;03m# src 경로 자동 등록 (PYTHONPATH 없이도 실행 가능)\u001b[39;00m\n\u001b[1;32m      7\u001b[0m sys\u001b[38;5;241m.\u001b[39mpath\u001b[38;5;241m.\u001b[39mappend(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124msrc\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[0;32m----> 9\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mossp_router\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mprotocol\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m (\n\u001b[1;32m     10\u001b[0m     load_bundled_policy,\n\u001b[1;32m     11\u001b[0m     load_input,\n\u001b[1;32m     12\u001b[0m     load_outcome,\n\u001b[1;32m     13\u001b[0m     parse_submission,\n\u001b[1;32m     14\u001b[0m )\n\u001b[1;32m     15\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mossp_router\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mscoring\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m score_submissions\n\u001b[1;32m     18\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21mmain\u001b[39m():\n\u001b[1;32m     19\u001b[0m     \u001b[38;5;66;03m# 1. Input, Outcomes, Policy 로드\u001b[39;00m\n",
      "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'ossp_router'"
     ]
    }
   ],
   "source": [
    "import json\n",
    "import os\n",
    "import sys\n",
    "from pathlib import Path\n",
    "\n",
    "# src 경로 자동 등록 (PYTHONPATH 없이도 실행 가능)\n",
    "sys.path.append(\"src\")\n",
    "\n",
    "from ossp_router.protocol import (\n",
    "    load_bundled_policy,\n",
    "    load_input,\n",
    "    load_outcome,\n",
    "    parse_submission,\n",
    ")\n",
    "from ossp_router.scoring import score_submissions\n",
    "\n",
    "\n",
    "def main():\n",
    "    # 1. Input, Outcomes, Policy 로드\n",
    "    inputs = load_input(Path(\"data/materialized/train/inputs.json\"))\n",
    "    outcomes = load_outcome(Path(\"data/train/outcomes.json\"))\n",
    "    policy = load_bundled_policy()\n",
    "\n",
    "    # 2. 앞서 생성한 3개 티어 제출 파일 로드\n",
    "    sub_paths = [\"sub_fast.json\", \"sub_balanced.json\", \"sub_premium.json\"]\n",
    "    submissions = []\n",
    "    for p in sub_paths:\n",
    "        with open(p, \"r\", encoding=\"utf-8\") as f:\n",
    "            submissions.append(parse_submission(json.load(f)))\n",
    "\n",
    "    # 3. 채점 수행 및 JSON 리포트 출력\n",
    "    report = score_submissions(inputs, outcomes, submissions, policy)\n",
    "    print(json.dumps(report, indent=2, ensure_ascii=False))\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8fb07808-4715-4dcb-a2b1-5cb457e96b66",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
