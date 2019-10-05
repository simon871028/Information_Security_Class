#include<iostream>
#include<iomanip>
#include<string>
#include<algorithm>
#include<math.h>
#include <vector>

using namespace std;

string caesar(string plain, int key)
{
	for (int i = 0; i < plain.length(); i++)
	{
		if (plain[i] >= 'a' && plain[i] <= 'z')
		{
			plain[i] = (plain[i] - 97 + key) % 26 + 97;
			plain[i] = toupper(plain[i]);
		}
	}
	return plain;
}

void playfair(string plain, string key)
{
	int c_size = plain.length(), k_size = key.length(), index = 0;
	int in_key[26];
	for (int i = 0; i < 26; i++)
		in_key[i] = -1;

	char arr[5][5] = { 0 };
	for (int i = 0; i < k_size; i++)
		key[i] = (char)tolower(key[i]);
	for (int i = 0; i < c_size; i++)
		if (plain[i] == 'j')
			plain[i] = 'i';
	for (int i = 0; i < k_size; i++)
		if (key[i] == 'j')
			key[i] = 'i';
	in_key['j' - 'a'] = 1;

	for (int i = 0; i < k_size; i++)
	{
		if (in_key[key[i] - 'a'] == -1)
		{
			in_key[key[i] - 'a'] = index;
			arr[index / 5][index % 5] = key[i];
			if (++index == 26) break;
		}
	}
	for (int i = 0; i < 26 && index < 26; i++)
	{
		if (in_key[i] == -1)
		{
			in_key[i] = index;
			arr[index / 5][index % 5] = i + 'a';
			index++;
		}
	}
	for (int i = 0; i < c_size; i += 2)
	{
		char first = plain[i], second = plain[i + 1];
		int f_key = in_key[first - 'a'], s_key = in_key[second - 'a'];

		if (f_key / 5 == s_key / 5)
			cout << (char)toupper(arr[f_key / 5][(f_key + 6) % 5]) << (char)toupper(arr[f_key / 5][(s_key + 6) % 5]);
		else if (f_key % 5 == s_key % 5)
			cout << (char)toupper(arr[((f_key / 5) + 6) % 5][f_key % 5]) << (char)toupper(arr[((s_key / 5) + 6) % 5][f_key % 5]);
		else
			cout << (char)toupper(arr[f_key / 5][s_key % 5]) << (char)toupper(arr[s_key / 5][f_key % 5]);
	}
}
void vernam(string plain, string key)
{
	while (plain.length() > key.length())
		key = key + key;
	//cout << key << endl;;
	int* XOR = new int[plain.length()];
	for (int i = 0; i < plain.length(); i++)
	{
		XOR[i] = (plain[i] - 97) ^ (key[i] - 65);
	}
	char* cypher = new char[plain.length()];
	for (int i = 0; i < plain.length(); i++)
	{
		cypher[i] = XOR[i] + 97;
		cypher[i] = toupper(cypher[i]);
		cout << cypher[i];
	}
	delete[]XOR;
	delete[]cypher;
}

void row(string plain, string key)
{
	int size = key.length();
	char** table = new char* [size];
	for (int i = 0; i < size; ++i)
		table[i] = new char[plain.length() / size + 1];
	//³Ðarray
	for (int j = 0; j < (plain.length() / size + 1); j++)
		for (int i = 0; i < size; i++)
			table[i][j] = 0;


	//¶ñ¤Jplaintext
	int index = 0;
	for (int j = 0; j < (plain.length() / size + 1); j++)
		for (int i = 0; i < size; i++)
		{
			if (index >= plain.length())
				break;
			table[i][j] = plain[index];
			index++;
		}
	for (size_t j = 1; j <= key.length(); j++)
	{
		for (int i = 0; i < key.length(); i++)
		{
			if (key[i] - '1' + 1 == j)
			{
				for (int x = 0; x < (plain.length() / size + 1); x++)
				{
					if (table[i][x] != 0)
						cout << (char)toupper(table[i][x]);
				}
			}
		}
	}
	for (size_t i = 0; i < size; i++)
		delete[] table[i];
	delete[] table;
}
string rail(string text, int key)
{
	// create the matrix 
	char** rail = new char* [key];
	for (int i = 0; i < key; ++i)
		rail[i] = new char[text.length()];

	for (int i = 0; i < key; i++)
		for (int j = 0; j < text.length(); j++)
			rail[i][j] = '\n';

	// to find the direction 
	bool down = false;
	int row = 0, col = 0;

	for (int i = 0; i < text.length(); i++)
	{
		if (row == 0 || row == key - 1)
			down = !down;
		rail[row][col++] = text[i];
		down ? row++ : row--;
	}
	string result;
	for (int i = 0; i < key; i++)
		for (int j = 0; j < text.length(); j++)
			if (rail[i][j] != '\n')
				result.push_back(rail[i][j]);
	for (int i = 0; i < result.length(); i++)
		result[i] = (char)toupper(result[i]);
	for (size_t i = 0; i < key; i++)
		delete[] rail[i];
	delete[] rail;
	return result;
}
int main(int argc, char* argv[])
{
	string plaintext = argv[3], method = argv[1], key = argv[2];
	//cin >> method;

	if (method == "caesar")
	{
		cout << caesar(plaintext, atoi(key.c_str()));
	}
	else if (method == "playfair")
	{
		playfair(plaintext, key);
	}
	else if (method == "vernam")
	{
		vernam(plaintext, key);
	}
	else if (method == "row")
	{
		row(plaintext, key);
	}
	else if (method == "rail_fence")
	{
		cout << rail(plaintext, atoi(key.c_str()));
	}
}