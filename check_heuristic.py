{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "e8498e81-6569-49d4-8ca5-a59e60c27236",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "===== Heuristic Score 결과 =====\n",
      "\n",
      "{'episode_id': 'train-0104', 'character_count': 59330, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 12}\n",
      "{'episode_id': 'train-0521', 'character_count': 65262, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 12}\n",
      "{'episode_id': 'train-0922', 'character_count': 59773, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 12}\n",
      "{'episode_id': 'train-0009', 'character_count': 65639, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0018', 'character_count': 58696, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0020', 'character_count': 60437, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0043', 'character_count': 65910, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0054', 'character_count': 67376, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0062', 'character_count': 53219, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0101', 'character_count': 64722, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0117', 'character_count': 63495, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0167', 'character_count': 64524, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0170', 'character_count': 60575, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0171', 'character_count': 50063, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0224', 'character_count': 65070, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0234', 'character_count': 63375, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0336', 'character_count': 59378, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0337', 'character_count': 64665, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0349', 'character_count': 64642, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0421', 'character_count': 63483, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': False, 'control_flow_count': 2, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0430', 'character_count': 61938, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0435', 'character_count': 56605, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0468', 'character_count': 63410, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0470', 'character_count': 67009, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0483', 'character_count': 61163, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0501', 'character_count': 56940, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0510', 'character_count': 54491, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': False, 'control_flow_count': 2, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0513', 'character_count': 61278, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0554', 'character_count': 50335, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n",
      "{'episode_id': 'train-0561', 'character_count': 65129, 'long_context': True, 'has_for': True, 'has_if': True, 'has_while': True, 'control_flow_count': 3, 'complexity_score': 11}\n"
     ]
    }
   ],
   "source": [
    "import sys\n",
    "from pathlib import Path\n",
    "\n",
    "sys.path.append(\"src\")\n",
    "\n",
    "from ossp_router.heuristic import extract_features, complexity_score\n",
    "from ossp_router.protocol import load_input\n",
    "\n",
    "\n",
    "def main():\n",
    "    inputs = load_input(\n",
    "        Path(\"data/materialized/train/inputs.json\")\n",
    "    )\n",
    "\n",
    "    results = []\n",
    "\n",
    "    for episode in inputs.episodes:\n",
    "        features = extract_features(episode)\n",
    "        score = complexity_score(features)\n",
    "\n",
    "        results.append({\n",
    "            \"episode_id\": episode.episode_id,\n",
    "            \"character_count\": features.character_count,\n",
    "            \"long_context\": features.long_context,\n",
    "            \"has_for\": features.has_for,\n",
    "            \"has_if\": features.has_if,\n",
    "            \"has_while\": features.has_while,\n",
    "            \"control_flow_count\": features.control_flow_count,\n",
    "            \"complexity_score\": score,\n",
    "        })\n",
    "\n",
    "    results.sort(\n",
    "        key=lambda x: x[\"complexity_score\"],\n",
    "        reverse=True\n",
    "    )\n",
    "\n",
    "    print(\"\\n===== Heuristic Score 결과 =====\\n\")\n",
    "\n",
    "    for row in results[:30]:\n",
    "        print(row)\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3b9de65a-0fc2-4d07-b1d2-8c983f3f65cb",
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
